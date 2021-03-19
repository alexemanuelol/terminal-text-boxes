#!/usr/bin/env python3

# Unicode source: https://en.wikipedia.org/wiki/List_of_Unicode_characters

# Lists of Unicode Characters

# Latin Scripts

BASIC_LATIN = [
    " ", "!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4",
    "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I",
    "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^",
    "_", "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
    "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~"
]

LATIN_1_SUPPLEMENT = [
    " ", "¡", "¢", "£", "¤", "¥", "¦", "§", "¨", "©", "ª", "«", "¬", "®", "¯", "°", "±", "²", "³", "´", "µ",
    "¶", "·", "¸", "¹", "º", "»", "¼", "½", "¾", "¿", "À", "Á", "Â", "Ã", "Ä", "Å", "Æ", "Ç", "È", "É", "Ê",
    "Ë", "Ì", "Í", "Î", "Ï", "Ð", "Ñ", "Ò", "Ó", "Ô", "Õ", "Ö", "×", "Ø", "Ù", "Ú", "Û", "Ü", "Ý", "Þ", "ß",
    "à", "á", "â", "ã", "ä", "å", "æ", "ç", "è", "é", "ê", "ë", "ì", "í", "î", "ï", "ð", "ñ", "ò", "ó", "ô",
    "õ", "ö", "÷", "ø", "ù", "ú", "û", "ü", "ý", "þ", "ÿ"
]

LATIN_EXTENDED_A = [
    "Ā", "ā", "Ă", "ă", "Ą", "ą", "Ć", "ć", "Ĉ", "ĉ", "Ċ", "ċ", "Č", "č", "Ď", "ď", "Đ", "đ", "Ē", "ē", "Ĕ",
    "ĕ", "Ė", "ė", "Ę", "ę", "Ě", "ě", "Ĝ", "ĝ", "Ğ", "ğ", "Ġ", "ġ", "Ģ", "ģ", "Ĥ", "ĥ", "Ħ", "ħ", "Ĩ", "ĩ",
    "Ī", "ī", "Ĭ", "ĭ", "Į", "į", "İ", "ı", "Ĳ", "ĳ", "Ĵ", "ĵ", "Ķ", "ķ", "ĸ", "Ĺ", "ĺ", "Ļ", "ļ", "Ľ", "ľ",
    "Ŀ", "ŀ", "Ł", "ł", "Ń", "ń", "Ņ", "ņ", "Ň", "ň", "ŉ", "Ŋ", "ŋ", "Ō", "ō", "Ŏ", "ŏ", "Ő", "ő", "Œ", "œ",
    "Ŕ", "ŕ", "Ŗ", "ŗ", "Ř", "ř", "Ś", "ś", "Ŝ", "ŝ", "Ş", "ş", "Š", "š", "Ţ", "ţ", "Ť", "ť", "Ŧ", "ŧ", "Ũ",
    "ũ", "Ū", "ū", "Ŭ", "ŭ", "Ů", "ů", "Ű", "ű", "Ų", "ų", "Ŵ", "ŵ", "Ŷ", "ŷ", "Ÿ", "Ź", "ź", "Ż", "ż", "Ž",
    "ž", "ſ"
]

LATIN_EXTENDED_B = [
    "ƀ", "Ɓ", "Ƃ", "ƃ", "Ƅ", "ƅ", "Ɔ", "Ƈ", "ƈ", "Ɖ", "Ɗ", "Ƌ", "ƌ", "ƍ", "Ǝ", "Ə", "Ɛ", "Ƒ", "ƒ", "Ɠ", "Ɣ",
    "ƕ", "Ɩ", "Ɨ", "Ƙ", "ƙ", "ƚ", "ƛ", "Ɯ", "Ɲ", "ƞ", "Ɵ", "Ơ", "ơ", "Ƣ", "ƣ", "Ƥ", "ƥ", "Ʀ", "Ƨ", "ƨ", "Ʃ",
    "ƪ", "ƫ", "Ƭ", "ƭ", "Ʈ", "Ư", "ư", "Ʊ", "Ʋ", "Ƴ", "ƴ", "Ƶ", "ƶ", "Ʒ", "Ƹ", "ƹ", "ƺ", "ƻ", "Ƽ", "ƽ", "ƾ",
    "ƿ", "ǀ", "ǁ", "ǂ", "ǃ", "Ǆ", "ǅ", "ǆ", "Ǉ", "ǈ", "ǉ", "Ǌ", "ǋ", "ǌ", "Ǎ", "ǎ", "Ǐ", "ǐ", "Ǒ", "ǒ", "Ǔ",
    "ǔ", "Ǖ", "ǖ", "Ǘ", "ǘ", "Ǚ", "ǚ", "Ǜ", "ǜ", "ǝ", "Ǟ", "ǟ", "Ǡ", "ǡ", "Ǣ", "ǣ", "Ǥ", "ǥ", "Ǧ", "ǧ", "Ǩ",
    "ǩ", "Ǫ", "ǫ", "Ǭ", "ǭ", "Ǯ", "ǯ", "ǰ", "Ǳ", "ǲ", "ǳ", "Ǵ", "ǵ", "Ƕ", "Ƿ", "Ǹ", "ǹ", "Ǻ", "ǻ", "Ǽ", "ǽ",
    "Ǿ", "ǿ", "Ȁ", "ȁ", "Ȃ", "ȃ", "Ȅ", "ȅ", "Ȇ", "ȇ", "Ȉ", "ȉ", "Ȋ", "ȋ", "Ȍ", "ȍ", "Ȏ", "ȏ", "Ȑ", "ȑ", "Ȓ",
    "ȓ", "Ȕ", "ȕ", "Ȗ", "ȗ", "Ș", "ș", "Ț", "ț", "Ȝ", "ȝ", "Ȟ", "ȟ", "Ƞ", "ȡ", "Ȣ", "ȣ", "Ȥ", "ȥ", "Ȧ", "ȧ",
    "Ȩ", "ȩ", "Ȫ", "ȫ", "Ȭ", "ȭ", "Ȯ", "ȯ", "Ȱ", "ȱ", "Ȳ", "ȳ", "ȴ", "ȵ", "ȶ", "ȷ", "ȸ", "ȹ", "Ⱥ", "Ȼ", "ȼ",
    "Ƚ", "Ⱦ", "ȿ", "ɀ", "Ɂ", "ɂ", "Ƀ", "Ʉ", "Ʌ", "Ɇ", "ɇ", "Ɉ", "ɉ", "Ɋ", "ɋ", "Ɍ", "ɍ", "Ɏ", "ɏ"
]

LATIN_EXTENDED_C = [
    "Ⱡ", "ⱡ", "Ɫ", "Ᵽ", "Ɽ", "ⱥ", "ⱦ", "Ⱨ", "ⱨ", "Ⱪ", "ⱪ", "Ⱬ", "ⱬ", "Ɑ", "Ɱ", "Ɐ", "Ɒ", "ⱱ", "Ⱳ", "ⱳ", "ⱴ",
    "Ⱶ", "ⱶ", "ⱷ", "ⱸ", "ⱹ", "ⱺ", "ⱻ", "ⱼ", "ⱽ", "Ȿ", "Ɀ"
]

LATIN_EXTENDED_D = [
    "꜠", "꜡", "Ꜣ", "ꜣ", "Ꜥ", "ꜥ", "Ꜧ", "ꜧ", "Ꜩ", "ꜩ", "Ꜫ", "ꜫ", "Ꜭ", "ꜭ", "Ꜯ", "ꜯ", "ꜰ", "ꜱ", "Ꜳ", "ꜳ", "Ꜵ",
    "ꜵ", "Ꜷ", "ꜷ", "Ꜹ", "ꜹ", "Ꜻ", "ꜻ", "Ꜽ", "ꜽ", "Ꜿ", "ꜿ", "Ꝁ", "ꝁ", "Ꝃ", "ꝃ", "Ꝅ", "ꝅ", "Ꝇ", "ꝇ", "Ꝉ", "ꝉ",
    "Ꝋ", "ꝋ", "Ꝍ", "ꝍ", "Ꝏ", "ꝏ", "Ꝑ", "ꝑ", "Ꝓ", "ꝓ", "Ꝕ", "ꝕ", "Ꝗ", "ꝗ", "Ꝙ", "ꝙ", "Ꝛ", "ꝛ", "Ꝝ", "ꝝ", "Ꝟ",
    "ꝟ", "Ꝡ", "ꝡ", "Ꝣ", "ꝣ", "Ꝥ", "ꝥ", "Ꝧ", "ꝧ", "Ꝩ", "ꝩ", "Ꝫ", "ꝫ", "Ꝭ", "ꝭ", "Ꝯ", "ꝯ", "ꝰ", "ꝱ", "ꝲ", "ꝳ",
    "ꝴ", "ꝵ", "ꝶ", "ꝷ", "ꝸ", "Ꝺ", "ꝺ", "Ꝼ", "ꝼ", "Ᵹ", "Ꝿ", "ꝿ", "Ꞁ", "ꞁ", "Ꞃ", "ꞃ", "Ꞅ", "ꞅ", "Ꞇ", "ꞇ", "ꞈ",
    "꞉", "꞊", "Ꞌ", "ꞌ", "Ɥ", "ꞎ", "ꞏ", "Ꞑ", "ꞑ", "Ꞓ", "ꞓ", "ꞔ", "ꞕ", "Ꞗ", "ꞗ", "Ꞙ", "ꞙ", "Ꞛ", "ꞛ", "Ꞝ", "ꞝ",
    "Ꞟ", "ꞟ", "Ꞡ", "ꞡ", "Ꞣ", "ꞣ", "Ꞥ", "ꞥ", "Ꞧ", "ꞧ", "Ꞩ", "ꞩ", "Ɦ", "Ɜ", "Ɡ", "Ɬ", "Ɪ", "ꞯ", "Ʞ", "Ʇ", "Ʝ",
    "Ꭓ", "Ꞵ", "ꞵ", "Ꞷ", "ꞷ", "Ꞹ", "ꞹ", "Ꞻ", "ꞻ", "Ꞽ", "ꞽ", "Ꞿ", "ꞿ", "Ꟃ", "ꟃ", "Ꞔ", "Ʂ", "Ᶎ", "Ꟈ", "ꟈ", "Ꟊ",
    "ꟊ", "Ꟶ", "ꟶ", "ꟷ", "ꟸ", "ꟹ", "ꟺ", "ꟻ", "ꟼ", "ꟽ", "ꟾ", "ꟿ"
]

LATIN_EXTENDED_E = [
    "ꬰ", "ꬱ", "ꬲ", "ꬳ", "ꬴ", "ꬵ", "ꬶ", "ꬷ", "ꬸ", "ꬹ", "ꬺ", "ꬻ", "ꬼ", "ꬽ", "ꬾ", "ꬿ", "ꭀ", "ꭁ", "ꭂ", "ꭃ", "ꭄ",
    "ꭅ", "ꭆ", "ꭇ", "ꭈ", "ꭉ", "ꭊ", "ꭋ", "ꭌ", "ꭍ", "ꭎ", "ꭏ", "ꭐ", "ꭑ", "ꭒ", "ꭓ", "ꭔ", "ꭕ", "ꭖ", "ꭗ", "ꭘ", "ꭙ",
    "ꭚ", "꭛", "ꭜ", "ꭝ", "ꭞ", "ꭟ", "ꭠ", "ꭡ", "ꭢ", "ꭣ", "ꭤ", "ꭥ", "ꭦ", "ꭧ", "ꭨ", "ꭩ", "꭪", "꭫"
]

LATIN_EXTENDED_ADDITIONAL = [
    "Ḃ", "ḃ", "Ḋ", "ḋ", "Ḟ", "ḟ", "Ṁ", "ṁ", "Ṗ", "ṗ", "Ṡ", "ṡ", "Ṫ", "ṫ", "Ẁ", "ẁ", "Ẃ", "ẃ", "Ẅ", "ẅ", "ẛ",
    "Ỳ", "ỳ"
]

# Phonetic Scripts

IPA_EXTENSIONS = [
    "ə", "ɼ", "ʒ"
]

SPACING_MODIFIER_LETTERS = [
    "ʰ", "ʱ", "ʲ", "ʳ", "ʴ", "ʵ", "ʶ", "ʷ", "ʸ", "ʹ", "ʺ", "ʻ", "ʼ", "ʽ", "ʾ", "ʿ", "ˀ", "ˁ", "˂", "˃", "˄",
    "˅", "ˆ", "ˇ", "ˈ", "ˉ", "ˊ", "ˋ", "ˌ", "ˍ", "ˎ", "ˏ", "ː", "ˑ", "˒", "˓", "˔", "˕", "˖", "˗", "˘", "˙",
    "˚", "˛", "˜", "˝", "˞ ", "˟", "ˠ", "ˡ", "ˢ", "ˣ", "ˤ", "˥", "˦", "˧", "˨", "˩", "˪", "˫", "ˬ", "˭", "ˮ",
    "˯", "˰", "˱", "˲", "˳", "˴", "˵", "˶", "˷", "˸", "˹", "˺", "˻", "˼", "˽", "˾", "˿"
]

PHONETIC_EXTENSIONS = [
    "ᴀ", "ᴁ", "ᴂ", "ᴃ", "ᴄ", "ᴅ", "ᴆ", "ᴇ", "ᴈ", "ᴉ", "ᴊ", "ᴋ", "ᴌ", "ᴍ", "ᴎ", "ᴏ", "ᴐ", "ᴑ", "ᴒ", "ᴓ", "ᴔ",
    "ᴕ", "ᴖ", "ᴗ", "ᴘ", "ᴙ", "ᴚ", "ᴛ", "ᴜ", "ᴝ", "ᴞ", "ᴟ", "ᴠ", "ᴡ", "ᴢ", "ᴣ", "ᴤ", "ᴥ", "ᴦ", "ᴧ", "ᴨ", "ᴩ",
    "ᴪ", "ᴫ", "ᴬ", "ᴭ", "ᴮ", "ᴯ", "ᴰ", "ᴱ", "ᴲ", "ᴳ", "ᴴ", "ᴵ", "ᴶ", "ᴷ", "ᴸ", "ᴹ", "ᴺ", "ᴻ", "ᴼ", "ᴽ", "ᴾ",
    "ᴿ", "ᵀ", "ᵁ", "ᵂ", "ᵃ", "ᵄ", "ᵅ", "ᵆ", "ᵇ", "ᵈ", "ᵉ", "ᵊ", "ᵋ", "ᵌ", "ᵍ", "ᵎ", "ᵏ", "ᵐ", "ᵑ", "ᵒ", "ᵓ",
    "ᵔ", "ᵕ", "ᵖ", "ᵗ", "ᵘ", "ᵙ", "ᵚ", "ᵛ", "ᵜ", "ᵝ", "ᵞ", "ᵟ", "ᵠ", "ᵡ", "ᵢ", "ᵣ", "ᵤ", "ᵥ", "ᵦ", "ᵧ", "ᵨ",
    "ᵩ", "ᵪ", "ᵫ", "ᵬ", "ᵭ", "ᵮ", "ᵯ", "ᵰ", "ᵱ", "ᵲ", "ᵳ", "ᵴ", "ᵵ", "ᵶ", "ᵷ", "ᵸ", "ᵹ", "ᵺ", "ᵻ", "ᵼ", "ᵽ",
    "ᵾ", "ᵿ"
]

PHONETIC_EXTENSIONS_SUPPLEMENT = [
    "ᶀ", "ᶁ", "ᶂ", "ᶃ", "ᶄ", "ᶅ", "ᶆ", "ᶇ", "ᶈ", "ᶉ", "ᶊ", "ᶋ", "ᶌ", "ᶍ", "ᶎ", "ᶏ", "ᶐ", "ᶑ", "ᶒ", "ᶓ", "ᶔ",
    "ᶕ", "ᶖ", "ᶗ", "ᶘ", "ᶙ", "ᶚ", "ᶛ", "ᶜ", "ᶝ", "ᶞ", "ᶟ", "ᶠ", "ᶡ", "ᶢ", "ᶣ", "ᶤ", "ᶥ", "ᶦ", "ᶧ", "ᶨ", "ᶩ",
    "ᶪ", "ᶫ", "ᶬ", "ᶭ", "ᶮ", "ᶯ", "ᶰ", "ᶱ", "ᶲ", "ᶳ", "ᶴ", "ᶵ", "ᶶ", "ᶷ", "ᶸ", "ᶹ", "ᶺ", "ᶻ", "ᶼ", "ᶽ", "ᶾ",
    "ᶿ"
]


# Combining Marks

COMBINING_DIACRITICAL_MARKS = [
    "◌᪰", "◌᪱", "◌᪲", "◌᪳", "◌᪴", "◌᪵", "◌᪶", "◌᪷", "◌᪸", "◌᪹", "◌᪺", "◌᪻", "◌᪼", "◌᪽", "◌᪾", "◌ᪿ", "◌ᫀ"
]

COMBINING_DIACRITICAL_MARKS_EXTENDED = [
    "◌︠", "◌︡", "◌︢", "◌︣", "◌︤", "◌︥", "◌︦", "◌︧", "◌︨", "◌︩", "◌︪", "◌︫", "◌︬", "◌︭", "◌︮", "◌︯"
]

COMBINING_HALF_MARKS = [
    "◌᷀", "◌᷁", "◌᷂", "◌᷃", "◌᷄", "◌᷅", "◌᷆", "◌᷇", "◌᷈", "◌᷉", "◌᷊", "◌᷋", "◌᷌", "◌᷍", "◌᷎", "◌᷏", "◌᷐", "◌᷑", "◌᷒", "◌ᷓ", "◌ᷔ",
    "◌ᷕ", "◌ᷖ", "◌ᷗ", "◌ᷘ", "◌ᷙ", "◌ᷚ", "◌ᷛ", "◌ᷜ", "◌ᷝ", "◌ᷞ", "◌ᷟ", "◌ᷠ", "◌ᷡ", "◌ᷢ", "◌ᷣ", "◌ᷤ", "◌ᷥ", "◌ᷦ", "◌ᷧ", "◌ᷨ", "◌ᷩ",
    "◌ᷪ", "◌ᷫ", "◌ᷬ", "◌ᷭ", "◌ᷮ", "◌ᷯ", "◌ᷰ", "◌ᷱ", "◌ᷲ", "◌ᷳ", "◌ᷴ", "◌᷵", "◌᷶", "◌᷷", "◌᷸", "◌᷹", "◌᷻", "◌᷼", "◌᷽", "◌᷾", "◌᷿"
]

COMBINING_DIACRITICAL_MARKS_SUPPLEMENT = [
    "◌⃐", "◌⃑", "◌⃒", "◌⃓", "◌⃔", "◌⃕", "◌⃖", "◌⃗", "◌⃘", "◌⃙", "◌⃚", "◌⃛", "◌⃜", "◌⃝", "◌⃞", "◌⃟", "◌⃠", "◌⃡", "◌⃢", "◌⃣", "◌⃤",
    "◌⃥", "◌⃦", "◌⃧", "◌⃨", "◌⃩", "◌⃪", "◌⃫", "◌⃬", "◌⃭", "◌⃮", "◌⃯", "◌⃰"
]

COMBINING_DIACRITICAL_MARKS_FOR_SYMBOLS = [
    "◌̀", "◌́", "◌̂", "◌̃", "◌̄", "◌̅", "◌̆", "◌̇", "◌̈", "◌̉", "◌̊", "◌̋", "◌̌", "◌̍", "◌̎", "◌̏", "◌̐", "◌̑", "◌̒", "◌̓", "◌̔",
    "◌̕", "◌̖", "◌̗", "◌̘", "◌̙", "◌̚", "◌̛", "◌̜", "◌̝", "◌̞", "◌̟", "◌̠", "◌̡", "◌̢", "◌̣", "◌̤", "◌̥", "◌̦", "◌̧", "◌̨", "◌̩",
    "◌̪", "◌̫", "◌̬", "◌̭", "◌̮", "◌̯", "◌̰", "◌̱", "◌̲", "◌̳", "◌̴", "◌̵", "◌̶", "◌̷", "◌̸", "◌̹", "◌̺", "◌̻", "◌̼", "◌̽", "◌̾",
    "◌̿", "◌̀", "◌́", "◌͂", "◌̓", "◌̈́", "◌ͅ", "◌͆", "◌͇", "◌͈", "◌͉", "◌͊", "◌͋", "◌͌", "◌͍", "◌͎", "הֽ͏ַ", "◌͐", "◌͑", "◌͒", "◌͓",
    "◌͔", "◌͕", "◌͖", "◌͗", "◌͘", "◌͙", "◌͚", "◌͛", "◌͜", "◌͝", "◌͞", "◌͟", "◌͠", "◌͡", "◌͢", "◌ͣ", "◌ͤ", "◌ͥ", "◌ͦ", "◌ͧ", "◌ͨ",
    "◌ͩ", "◌ͪ", "◌ͫ", "◌ͬ", "◌ͭ", "◌ͮ", "◌ͯ"
]

# Greek and Coptic

GREEK_AND_COPTIC = [
    "Ͱ", "ͱ", "Ͳ", "ͳ", "ʹ", "͵", "Ͷ", "ͷ", "ͺ", "ͻ", "ͼ", "ͽ", ";", "Ϳ", "΄", "΅", "Ά", "·", "Έ", "Ή", "Ί",
    "Ό", "Ύ", "Ώ", "ΐ", "Α", "Β", "Γ", "Δ", "Ε", "Ζ", "Η", "Θ", "Ι", "Κ", "Λ", "Μ", "Ν", "Ξ", "Ο", "Π", "Ρ",
    "Σ", "Τ", "Υ", "Φ", "Χ", "Ψ", "Ω", "Ϊ", "Ϋ", "ά", "έ", "ή", "ί", "ΰ", "α", "β", "γ", "δ", "ε", "ζ", "η",
    "θ", "ι", "κ", "λ", "μ", "ν", "ξ", "ο", "π", "ρ", "ς", "σ", "τ", "υ", "φ", "χ", "ψ", "ω", "ϊ", "ϋ", "ό",
    "ύ", "ώ", "Ϗ", "ϐ", "ϑ", "ϒ", "ϓ", "ϔ", "ϕ", "ϖ", "ϗ", "Ϙ", "ϙ", "Ϛ", "ϛ", "Ϝ", "ϝ", "Ϟ", "ϟ", "Ϡ", "ϡ",
    "Ϣ", "ϣ", "Ϥ", "ϥ", "Ϧ", "ϧ", "Ϩ", "ϩ", "Ϫ", "ϫ", "Ϭ", "ϭ", "Ϯ", "ϯ", "ϰ", "ϱ", "ϲ", "ϳ", "ϴ", "ϵ", "϶",
    "Ϸ", "ϸ", "Ϲ", "Ϻ", "ϻ", "ϼ", "Ͻ", "Ͼ", "Ͽ"
]

GREEK_EXTENDED = [
    "ἀ", "ἁ", "ἂ", "ἃ", "ἄ", "ἅ", "ἆ", "ἇ", "Ἀ", "Ἁ", "Ἂ", "Ἃ", "Ἄ", "Ἅ", "Ἆ", "Ἇ", "ἐ", "ἑ", "ἒ", "ἓ", "ἔ",
    "ἕ", "Ἐ", "Ἑ", "Ἒ", "Ἓ", "Ἔ", "Ἕ", "ἠ", "ἡ", "ἢ", "ἣ", "ἤ", "ἥ", "ἦ", "ἧ", "Ἠ", "Ἡ", "Ἢ", "Ἣ", "Ἤ", "Ἥ",
    "Ἦ", "Ἧ", "ἰ", "ἱ", "ἲ", "ἳ", "ἴ", "ἵ", "ἶ", "ἷ", "Ἰ", "Ἱ", "Ἲ", "Ἳ", "Ἴ", "Ἵ", "Ἶ", "Ἷ", "ἠ", "ἡ", "ἢ",
    "ἣ", "ἤ", "ἥ", "ἦ", "ἧ", "Ἠ", "Ἡ", "Ἢ", "Ἣ", "Ἤ", "Ἥ", "Ἦ", "Ἧ", "ἰ", "ἱ", "ἲ", "ἳ", "ἴ", "ἵ", "ἶ", "ἷ",
    "Ἰ", "Ἱ", "Ἲ", "Ἳ", "Ἴ", "Ἵ", "Ἶ", "Ἷ", "ὀ", "ὁ", "ὂ", "ὃ", "ὄ", "ὅ", "Ὀ", "Ὁ", "Ὂ", "Ὃ", "Ὄ", "Ὅ", "ὐ",
    "ὑ", "ὒ", "ὓ", "ὔ", "ὕ", "ὖ", "ὗ", "Ὑ", "Ὓ", "Ὕ", "Ὗ", "ὠ", "ὡ", "ὢ", "ὣ", "ὤ", "ὥ", "ὦ", "ὧ", "Ὠ", "Ὡ",
    "Ὢ", "Ὣ", "Ὤ", "Ὥ", "Ὦ", "Ὧ", "ὰ", "ά", "ὲ", "έ", "ὴ", "ή", "ὶ", "ί", "ὸ", "ό", "ὺ", "ύ", "ὼ", "ώ", "ᾀ",
    "ᾁ", "ᾂ", "ᾃ", "ᾄ", "ᾅ", "ᾆ", "ᾇ", "ᾈ", "ᾉ", "ᾊ", "ᾋ", "ᾌ", "ᾍ", "ᾎ", "ᾏ", "ᾐ", "ᾑ", "ᾒ", "ᾓ", "ᾔ", "ᾕ",
    "ᾖ", "ᾗ", "ᾘ", "ᾙ", "ᾚ", "ᾛ", "ᾜ", "ᾝ", "ᾞ", "ᾟ", "ᾠ", "ᾡ", "ᾢ", "ᾣ", "ᾤ", "ᾥ", "ᾦ", "ᾧ", "ᾨ", "ᾩ", "ᾪ",
    "ᾫ", "ᾬ", "ᾭ", "ᾮ", "ᾯ", "ᾰ", "ᾱ", "ᾲ", "ᾳ", "ᾴ", "ᾶ", "ᾷ", "Ᾰ", "Ᾱ", "Ὰ", "Ά", "ᾼ", "᾽", "ι", "᾿", "῀",
    "῁", "ῂ", "ῃ", "ῄ", "ῆ", "ῇ", "Ὲ", "Έ", "Ὴ", "Ή", "ῌ", "῍", "῎", "῏", "ῐ", "ῑ", "ῒ", "ΐ", "ῖ", "ῗ", "Ῐ",
    "Ῑ", "Ὶ", "Ί", "῝", "῞", "῟", "ῠ", "ῡ", "ῢ", "ΰ", "ῤ", "ῥ", "ῦ", "ῧ", "Ῠ", "Ῡ", "Ὺ", "Ύ", "Ῥ", "῭", "΅",
    "`", "ῲ", "ῳ", "ῴ", "ῶ", "ῷ", "Ὸ", "Ό", "Ὼ", "Ώ", "ῼ", "´", "῾"
]

CYRILLIC = [
    "Ѐ", "Ё", "Ђ", "Ѓ", "Є", "Ѕ", "І", "Ї", "Ј", "Љ", "Њ", "Ћ", "Ќ", "Ѝ", "Ў", "Џ", "А", "Б", "В", "Г", "Д",
    "Е", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ",
    "Ъ", "Ы", "Ь", "Э", "Ю", "Я", "а", "б", "в", "г", "д", "е", "ж", "з", "и", "й", "к", "л", "м", "н", "о",
    "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я", "ѐ", "ё", "ђ", "ѓ",
    "є", "ѕ", "і", "ї", "ј", "љ", "њ", "ћ", "ќ", "ѝ", "ў", "џ", "Ѡ", "ѡ", "Ѣ", "ѣ", "Ѥ", "ѥ", "Ѧ", "ѧ", "Ѩ",
    "ѩ", "Ѫ", "ѫ", "Ѭ", "ѭ", "Ѯ", "ѯ", "Ѱ", "ѱ", "Ѳ", "ѳ", "Ѵ", "ѵ", "Ѷ", "ѷ", "Ѹ", "ѹ", "Ѻ", "ѻ", "Ѽ", "ѽ",
    "Ѿ", "ѿ", "Ҁ", "ҁ", "҂", " ҃", " ҄", " ҅", " ҆", " ҇", " ", " ", "Ҋ", "ҋ", "Ҍ", "ҍ", "Ҏ", "ҏ", "Ґ", "ґ", "Ғ",
    "ғ", "Ҕ", "ҕ", "Җ", "җ", "Ҙ", "ҙ", "Қ", "қ", "Ҝ", "ҝ", "Ҟ", "ҟ", "Ҡ", "ҡ", "Ң", "ң", "Ҥ", "ҥ", "Ҧ", "ҧ",
    "Ҩ", "ҩ", "Ҫ", "ҫ", "Ҭ", "ҭ", "Ү", "ү", "Ұ", "ұ", "Ҳ", "ҳ", "Ҵ", "ҵ", "Ҷ", "ҷ", "Ҹ", "ҹ", "Һ", "һ", "Ҽ",
    "ҽ", "Ҿ", "ҿ", "Ӏ", "Ӂ", "ӂ", "Ӄ", "ӄ", "Ӆ", "ӆ", "Ӈ", "ӈ", "Ӊ", "ӊ", "Ӌ", "ӌ", "Ӎ", "ӎ", "ӏ", "Ӑ", "ӑ",
    "Ӓ", "ӓ", "Ӕ", "ӕ", "Ӗ", "ӗ", "Ә", "ә", "Ӛ", "ӛ", "Ӝ", "ӝ", "Ӟ", "ӟ", "Ӡ", "ӡ", "Ӣ", "ӣ", "Ӥ", "ӥ", "Ӧ",
    "ӧ", "Ө", "ө", "Ӫ", "ӫ", "Ӭ", "ӭ", "Ӯ", "ӯ", "Ӱ", "ӱ", "Ӳ", "ӳ", "Ӵ", "ӵ", "Ӷ", "ӷ", "Ӹ", "ӹ", "Ӻ", "ӻ",
    "Ӽ", "ӽ", "Ӿ", "ӿ"
]

CYRILLIC_SUPPLEMENT = [
    "Ԁ", "ԁ", "Ԃ", "ԃ", "Ԅ", "ԅ", "Ԇ", "ԇ", "Ԉ", "ԉ", "Ԋ", "ԋ", "Ԍ", "ԍ", "Ԏ", "ԏ", "Ԑ", "ԑ", "Ԓ", "ԓ", "Ԕ",
    "ԕ", "Ԗ", "ԗ", "Ԙ", "ԙ", "Ԛ", "ԛ", "Ԝ", "ԝ", "Ԟ", "ԟ", "Ԡ", "ԡ", "Ԣ", "ԣ", "Ԥ", "ԥ", "Ԧ", "ԧ", "Ԩ", "ԩ",
    "Ԫ", "ԫ", "Ԭ", "ԭ", "Ԯ", "ԯ"
]

CYRILLIC_EXTENDED_A = [
    " ⷠ", " ⷡ", " ⷢ", " ⷣ", " ⷤ", " ⷥ", " ⷦ", " ⷧ", " ⷨ", " ⷩ", " ⷪ", " ⷫ", " ⷬ", " ⷭ", " ⷮ", " ⷯ", " ⷰ", " ⷱ", " ⷲ", " ⷳ", " ⷴ",
    " ⷵ", " ⷶ", " ⷷ", " ⷸ", " ⷹ", " ⷺ", " ⷻ", " ⷼ", " ⷽ", " ⷾ", " ⷿ"
]

CYRILLIC_EXTENDED_B = [
    "Ꙁ", "ꙁ", "Ꙃ", "ꙃ", "Ꙅ", "ꙅ", "Ꙇ", "ꙇ", "Ꙉ", "ꙉ", "Ꙋ", "ꙋ", "Ꙍ", "ꙍ", "Ꙏ", "ꙏ", "Ꙑ", "ꙑ", "Ꙓ", "ꙓ", "Ꙕ",
    "ꙕ", "Ꙗ", "ꙗ", "Ꙙ", "ꙙ", "Ꙛ", "ꙛ", "Ꙝ", "ꙝ", "Ꙟ", "ꙟ", "Ꙡ", "ꙡ", "Ꙣ", "ꙣ", "Ꙥ", "ꙥ", "Ꙧ", "ꙧ", "Ꙩ", "ꙩ",
    "Ꙫ", "ꙫ", "Ꙭ", "ꙭ", "ꙮ", " ꙯", " ꙰", " ꙱", " ꙲", "꙳", " ꙴ", " ꙵ", " ꙶ", " ꙷ", " ꙸ", " ꙹ", " ꙺ", " ꙻ", " ꙼", " ꙽", "꙾",
    "ꙿ", "Ꚁ", "ꚁ", "Ꚃ", "ꚃ", "Ꚅ", "ꚅ", "Ꚇ", "ꚇ", "Ꚉ", "ꚉ", "Ꚋ", "ꚋ", "Ꚍ", "ꚍ", "Ꚏ", "ꚏ", "Ꚑ", "ꚑ", "Ꚓ", "ꚓ",
    "Ꚕ", "ꚕ", "Ꚗ", "ꚗ", "Ꚙ", "ꚙ", "Ꚛ", "ꚛ", "ꚜ", "ꚝ", " ꚞ", " ꚟ"
]

CYRILLIC_EXTENDED_C = [
    "ᲀ", "ᲁ", "ᲂ", "ᲃ", "ᲄ", "ᲅ", "ᲆ", "ᲇ", "ᲈ"
]


ALL_UNICODE =   BASIC_LATIN + \
                LATIN_1_SUPPLEMENT + \
                LATIN_EXTENDED_A + \
                LATIN_EXTENDED_B + \
                LATIN_EXTENDED_C + \
                LATIN_EXTENDED_D + \
                LATIN_EXTENDED_E + \
                LATIN_EXTENDED_ADDITIONAL + \
                IPA_EXTENSIONS + \
                SPACING_MODIFIER_LETTERS + \
                PHONETIC_EXTENSIONS + \
                PHONETIC_EXTENSIONS_SUPPLEMENT + \
                COMBINING_DIACRITICAL_MARKS + \
                COMBINING_DIACRITICAL_MARKS_EXTENDED + \
                COMBINING_HALF_MARKS + \
                COMBINING_DIACRITICAL_MARKS_SUPPLEMENT + \
                COMBINING_DIACRITICAL_MARKS_FOR_SYMBOLS + \
                GREEK_AND_COPTIC + \
                GREEK_EXTENDED + \
                CYRILLIC + \
                CYRILLIC_SUPPLEMENT + \
                CYRILLIC_EXTENDED_A + \
                CYRILLIC_EXTENDED_B + \
                CYRILLIC_EXTENDED_C



def isUnicode(character):
    """ Returns true if char i unicode. """
    if character in ALL_UNICODE:
        return True
    else:
        return False
