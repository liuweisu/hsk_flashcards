"""Pinyin generator: lexicon-driven segmentation + sandhi + erhua.
Validated against 1193 hand-written gold sentences."""
import json, re
from pypinyin import pinyin, Style

SRC = '/home/claude/clem109/hsk-vocabulary/hsk-vocab-json'

LEX = {}
for lv in range(1, 7):
    for e in json.load(open(f'{SRC}/hsk-level-{lv}.json')):
        LEX.setdefault(e['hanzi'], e['pinyin'].strip())

# words the HSK list lacks or renders differently from standard orthography
EXTRA = {
    '一下': 'yī xià', '一点儿': 'yī diǎn r', '点儿': 'diǎn r', '这儿': 'zhè r', '那儿': 'nà r',
    '哪儿': 'nǎ r', '一会儿': 'yī huì r', '好玩儿': 'hǎo wán r', '玩儿': 'wán r',
    '我们': 'wǒ men', '你们': 'nǐ men', '他们': 'tā men', '她们': 'tā men', '咱们': 'zán men',
    '孩子们': 'hái zi men', '人们': 'rén men', '同学们': 'tóng xué men',
    '一起': 'yī qǐ', '一共': 'yī gòng', '一样': 'yī yàng', '一般': 'yī bān', '一边': 'yī biān',
    '一直': 'yī zhí', '一定': 'yī dìng', '一切': 'yī qiè', '一些': 'yī xiē', '一路': 'yī lù',
    '不客气': 'bú kè qi', '对不起': 'duì bu qǐ', '没关系': 'méi guān xi',
    '个子': 'gè zi', '真正': 'zhēn zhèng', '正好': 'zhèng hǎo',
    '先生': 'xiān sheng', '小姐': 'xiǎo jiě', '朋友': 'péng you', '衣服': 'yī fu',
    '谢谢': 'xiè xie', '休息': 'xiū xi', '事情': 'shì qing', '明白': 'míng bai',
    '便宜': 'pián yi', '意思': 'yì si', '告诉': 'gào su', '清楚': 'qīng chu',
    '暖和': 'nuǎn huo', '凉快': 'liáng kuai', '舒服': 'shū fu', '聪明': 'cōng ming',
    '热闹': 'rè nao', '麻烦': 'má fan', '客气': 'kè qi', '关系': 'guān xi',
    '故事': 'gù shi', '消息': 'xiāo xi', '精神': 'jīng shen', '打扮': 'dǎ ban',
    '收拾': 'shōu shi', '商量': 'shāng liang', '安静': 'ān jìng', '活泼': 'huó po',
    '马虎': 'mǎ hu', '厉害': 'lì hai', '困难': 'kùn nan', '知识': 'zhī shi',
    '态度': 'tài du', '力气': 'lì qi', '脾气': 'pí qi', '咳嗽': 'ké sou',
    '大夫': 'dài fu', '师傅': 'shī fu', '亲戚': 'qīn qi', '葡萄': 'pú tao',
    '钥匙': 'yào shi', '地方': 'dì fang', '姑娘': 'gū niang', '裤子': 'kù zi',
    '窗户': 'chuāng hu', '福气': 'fú qi', '热情': 'rè qíng', '认真': 'rèn zhēn',
    '晚上': 'wǎn shang', '早上': 'zǎo shang', '身上': 'shēn shang', '头发': 'tóu fa',
    '时间': 'shí jiān', '星期': 'xīng qī', '因为': 'yīn wèi', '咖啡': 'kā fēi',
    '后面': 'hòu miàn', '前面': 'qián miàn', '上面': 'shàng miàn', '下面': 'xià miàn',
    '里面': 'lǐ miàn', '外面': 'wài miàn', '对面': 'duì miàn', '旁边': 'páng biān',
    '大学生': 'dà xué shēng', '打篮球': 'dǎ lán qiú', '打电话': 'dǎ diàn huà',
    '中学生': 'zhōng xué shēng', '小学生': 'xiǎo xué shēng',
    '早点儿': 'zǎo diǎn r', '晚点儿': 'wǎn diǎn r', '有点儿': 'yǒu diǎn r',
    '第一': 'dì yī', '第二': 'dì èr', '第三': 'dì sān',
    '这里': 'zhè lǐ', '那里': 'nà lǐ', '哪里': 'nǎ lǐ', '没有': 'méi yǒu',
    '楼房': 'lóu fáng', '女儿': 'nǚ ér', '儿子': 'ér zi', '画儿': 'huà r',
    '常常': 'cháng cháng', '夏天': 'xià tiān', '春天': 'chūn tiān', '秋天': 'qiū tiān',
    '冬天': 'dōng tiān', '白天': 'bái tiān', '每天': 'měi tiān',
    '长得': 'zhǎng de', '值得': 'zhí dé', '觉得': 'jué de', '起来': 'qǐ lái', '过来': 'guò lái', '出去': 'chū qù', '进来': 'jìn lái',
    '回来': 'huí lái', '下去': 'xià qù', '得到': 'dé dào', '长大': 'zhǎng dà',
    '不过': 'bú guò', '不但': 'bú dàn', '不错': 'bú cuò', '不要': 'bú yào',
    '不是': 'bú shì', '不用': 'bú yòng', '不会': 'bú huì', '不在': 'bú zài',
    '小时候': 'xiǎo shí hou', '笑话': 'xiào hua',
    '看看': 'kàn kan', '走走': 'zǒu zou', '尝尝': 'cháng chang', '想想': 'xiǎng xiang',
    '说说': 'shuō shuo', '试试': 'shì shi', '坐坐': 'zuò zuo', '等等': 'děng deng',
    '公共': 'gōng gòng', '服务费': 'fú wù fèi', '公共汽车': 'gōng gòng qì chē',
    '这些': 'zhè xiē', '那些': 'nà xiē', '哪些': 'nǎ xiē', '从小': 'cóng xiǎo',
    '一篇': 'yī piān', '服务': 'fú wù', '工作人员': 'gōng zuò rén yuán',
    '玻璃': 'bō li', '沙发': 'shā fā', '护士': 'hù shi', '姑姑': 'gū gu',
}
for bad in ('个人', '个子儿', '一点'):
    LEX.pop(bad, None)
LEX.update(EXTRA)
LEX['喂'] = 'wéi'

# single characters whose default reading differs in context
NEUTRAL_PARTICLE = {'的': 'de', '了': 'le', '着': 'zhe', '吗': 'ma', '呢': 'ne',
                    '吧': 'ba', '啊': 'a', '呀': 'ya', '们': 'men', '个': 'ge'}
MAXLEN = max(len(w) for w in LEX)

PUNCT = {'，': ',', '。': '.', '？': '?', '！': '!', '、': ',', '；': ';',
         '：': ':', '“': '', '”': '', '‘': '', '’': '', '（': '(', '）': ')'}
VOWELS = 'aeiouüāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ'


def tone_of(syl):
    """Return 1-4, or 5 for neutral (no tone mark)."""
    marks = {'āēīōūǖ': 1, 'áéíóúǘ': 2, 'ǎěǐǒǔǚ': 3, 'àèìòùǜ': 4}
    for chars, t in marks.items():
        if any(c in syl for c in chars):
            return t
    return 5


def segment(text):
    """Greedy longest-match against the HSK lexicon."""
    out, i = [], 0
    while i < len(text):
        ch = text[i]
        if not '一' <= ch <= '鿿':
            out.append((ch, None)); i += 1; continue
        for L in range(min(MAXLEN, len(text) - i), 0, -1):
            w = text[i:i + L]
            if w in LEX:
                out.append((w, LEX[w])); i += L; break
        else:
            out.append((ch, None)); i += 1
    return out


def syls_for(word, py):
    if py:
        return py.split()
    return [x[0] for x in pinyin(word, style=Style.TONE)]


def generate(text):
    segs = segment(text)
    # flatten to (hanzi_char, syllable, word_index)
    flat = []
    for wi, (w, py) in enumerate(segs):
        if not '一' <= w[0] <= '鿿':
            flat.append((w, None, wi)); continue
        sy = syls_for(w, py)
        if len(sy) != len(w):  # fall back per-char on mismatch
            sy = [x[0] for x in pinyin(w, style=Style.TONE)]
        for c, s in zip(w, sy):
            flat.append((c, s, wi))

    # --- single-character contextual overrides ---
    for i, (c, s, wi) in enumerate(flat):
        if s is None:
            continue
        nxt = next((flat[j] for j in range(i + 1, len(flat)) if flat[j][1]), None)
        prev = next((flat[j] for j in range(i - 1, -1, -1) if flat[j][1]), None)
        single = len([1 for x in flat if x[2] == wi]) == 1

        if c in NEUTRAL_PARTICLE and single:
            # 个 keeps gè only in 个子-type words (handled by lexicon), else neutral
            flat[i] = (c, NEUTRAL_PARTICLE[c], wi)
            s = flat[i][1]
        if c == '只' and single:
            # adverb "only" before a verb, vs measure word after a number
            prev_num = prev and prev[0] in '一二三四五六七八九十两几这那每'
            flat[i] = (c, 'zhī' if prev_num else 'zhǐ', wi)
        if c == '得' and single and prev:
            flat[i] = (c, 'de', wi)   # structural particle (他说得很好)
        if c == '过' and single and prev and prev[0] not in '，。？！':
            flat[i] = (c, 'guo', wi); s = 'guo'
        if c == '不' and single and nxt:
            flat[i] = (c, 'bú' if tone_of(nxt[1]) == 4 else 'bù', wi)
        # 一 takes no sandhi inside a number (十一, 二十一) or as an ordinal
        prev_is_digit = prev and prev[0] in '〇零一二三四五六七八九十百千万亿第'
        if c == '一' and single and nxt and not prev_is_digit:
            tt = tone_of(nxt[1])
            flat[i] = (c, 'yí' if tt == 4 else ('yì' if tt in (1, 2, 3) else 'yī'), wi)

    # --- 一 inside lexicon words (一起 yìqǐ, 一下 yíxià ...) ---
    for i, (c, s, wi) in enumerate(flat):
        if c == '一' and s and s.startswith('y') and not single_char(flat, wi):
            nxt = flat[i + 1] if i + 1 < len(flat) and flat[i + 1][2] == wi else None
            if nxt and nxt[1]:
                t = tone_of(nxt[1])
                flat[i] = (c, 'yí' if t == 4 else ('yì' if t in (1, 2, 3) else 'yī'), wi)

    # --- standalone trailing 儿 becomes erhua on the previous word ---
    merged = []
    for i, (c, s, wi) in enumerate(flat):
        if c == '儿' and s and merged and single_char(flat, wi):
            pc, ps, pwi = merged[-1]
            if ps and not ps.endswith('r'):
                merged[-1] = (pc, ps + 'r', pwi)
                continue
        merged.append((c, s, wi))
    flat = merged

    # --- assemble: join syllables inside a word, space between words ---
    parts, cur_wi, buf = [], None, ''
    for c, s, wi in flat:
        if s is None:
            if buf: parts.append(buf); buf = ''
            p = PUNCT.get(c, c)
            if p: parts.append(('PUNCT', p))
            cur_wi = None
            continue
        if wi != cur_wi:
            if buf: parts.append(buf)
            buf = s; cur_wi = wi
        else:
            buf = join_syl(buf, s)
    if buf: parts.append(buf)

    out = ''
    for p in parts:
        if isinstance(p, tuple):
            out = out.rstrip() + p[1] + ' '
        else:
            out += p + ' '
    out = out.strip()
    return out[:1].upper() + out[1:] if out else out


def single_char(flat, wi):
    return len([1 for x in flat if x[2] == wi]) == 1


TONELESS = str.maketrans('āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ', 'aaaaeeeeiiiioooouuuuüüüü')


def strip_tone(s):
    return s.translate(TONELESS)


def join_syl(a, b):
    """Join two syllables inside one word, inserting ' where ambiguous."""
    if not a: return b
    if b == 'r':
        return a + 'r'
    if b and b[0] in VOWELS and a[-1] in VOWELS + 'nNgG':
        return a + "'" + b
    return a + b


if __name__ == '__main__':
    deck = json.load(open('deck14.json'))
    norm = lambda x: re.sub(r"[\s,.?!;:'’]", '', x.lower())
    exact = 0; diffs = []
    for r in deck:
        g = generate(r['s'])
        if norm(g) == norm(r['sp']): exact += 1
        else: diffs.append((r['s'], r['sp'], g))
    print(f'syllable-exact: {exact}/{len(deck)} = {100*exact/len(deck):.1f}%')
    print(f'mismatches: {len(diffs)}')
    for d in diffs[:30]:
        print('  ', d[0], '\n     gold:', d[1], '\n     gen :', d[2])
