edge_cases = {

    "homoglyphs": [
        # Cyrillic letters that look like Latin
        "Latin a vs Cyrillic а: cafe vs саfе",
        "Latin e vs Cyrillic е: test vs тeст",
        "Latin o vs Cyrillic о: code vs соde",
        "Latin p vs Cyrillic р: paper vs рарer",
        "Mixed script word: раython (р is Cyrillic, rest Latin)",
        "аррlе (all Cyrillic homoglyphs for 'apple')",
        "Gооgle (ооg are Cyrillic о)",
        "microsоft (о is Cyrillic)",
        "exаmple.cоm (а and о are Cyrillic)",
        "НОѠ аrе yоu? (mixed homoglyphs)",
        # Greek homoglyphs
        "Greek Α vs Latin A: ΑΒΓ looks like ABT",
        "Greek Κ vs Latin K",
        "Greek Ν vs Latin N",
        "Greek Ρ vs Latin P",
        "Greek Τ vs Latin T",
        # Math homoglyphs
        "× (multiplication) vs x (letter)",
        "∗ (asterism) vs * (asterisk)",
        "− (minus) vs - (hyphen) vs ‐ (hyphen) vs – (en dash) vs — (em dash)",
    ],

    "zero_width_characters": [
        "word\u200bbreak",         # zero-width space
        "non\u200cjoiner",         # zero-width non-joiner
        "zero\u200dwidth",         # zero-width joiner
        "\ufefffeff start",        # BOM (byte order mark)
        "left\u202aright",         # left-to-right embedding
        "right\u202bright",        # right-to-left embedding
        "\u2060word\u2060joiner",  # word joiner
        "invis\u2062ible\u2063",   # invisible separator
        "normal\u00adsoft\u00adhyphen",  # soft hyphen
        "zero\u034fwidth\u034fjoiner",   # combining grapheme joiner
        # Strings that look empty but aren't
        "\u200b",
        "\u200c\u200d\u200e\u200f",
        "\ufeff",
        " \u00a0\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a",  # various spaces
        "\u3000",  # ideographic space
    ],

    "rtl_ltr_mixing": [
        "Hello مرحبا World",
        "English then עברית then English",
        "مرحبا Hello مرحبا",
        "1 + ٢ = 3",
        "Price: $50 or ٥٠ USD",
        "( أهلا وسهلا )",
        "AI هوش مصنوعی AI",
        "foo بار baz",
        "LTR: text العربية RTL",
        "\u202aLTR override\u202c",
        "\u202bRTL override\u202c",
        "mixed: hello שלום مرحبا नमस्ते 你好",
        "Email: test@example.com :البريد",
        "Parentheses: (أهلا) and (hello)",
        "Numbers: ١٢٣ and 123 in same sentence",
    ],

    "diacritics_and_special_latin": [
        # Combining diacritics (base char + combining mark vs precomposed)
        "cafe\u0301",              # café via combining acute
        "café",                    # café precomposed
        "na\u0308ive",            # naïve via combining diaeresis
        "naïve",                  # naïve precomposed
        # Various diacritic forms
        "Héllo Wörld",
        "Ñoño, niño",
        "Ångström: Å",
        "Résumé, naïve, coöperate, fiancée",
        "Über, über, Straße, schön",
        "Crème brûlée, entrée, exposé",
        "Fête, château, rôle, hôtel",
        "Piñata, jalapeño, señor",
        "Søren Kierkegaard, Niels Bohr",
        "Håkon, Björn, Sigurður",
        # Ligatures
        "æsthetics and Œdipus",
        "ﬁne ﬂight ﬀ",  # fi, fl, ff ligatures
        "st ﬅ",
        "ĳ (Dutch ij ligature)",
        # Unusual letters
        "ß (German sharp s) = ss",
        "Ð ð (eth), Þ þ (thorn)",
        "Ŋ ŋ (eng)",
        "Ə ə (schwa)",
    ],

    "whitespace_variants": [
        "normal space: hello world",
        "no-break space: hello\u00a0world",
        "en space: hello\u2002world",
        "em space: hello\u2003world",
        "thin space: hello\u2009world",
        "hair space: hello\u200aworld",
        "ideographic space: hello\u3000world",
        "figure space: hello\u2007world",
        "tab\there",
        "newline\nhere",
        "carriage return\rhere",
        "form feed\x0chere",
        "vertical tab\x0bhere",
        "multiple    spaces    between    words",
        "trailing spaces   ",
        "   leading spaces",
        "\t\t\ttabs leading",
        "mixed \t whitespace \n types \r\n combined",
        "NBSP: it\u00a0doesn't\u00a0break\u00a0here",
        "\n\n\n multiple \n\n\n newlines \n\n\n",
    ],

    "long_tokens": [
        # URLs
        "https://www.example.com/very/long/path/to/some/resource?param1=value1&param2=value2&param3=value3#section",
        "https://api.github.com/repos/owner/repository/pulls?state=open&base=main&sort=created&direction=desc&per_page=100",
        # Base64
        "SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBiYXNlNjQgZW5jb2RlZCBzdHJpbmcgZm9yIHRlc3Rpbmcgcm91Z2hseSA2NCBieXRlcw==",
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
        # UUIDs and hashes
        "550e8400-e29b-41d4-a716-446655440000",
        "sha256:a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
        "git:7f3a4b8c9d2e1f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9",
        # Long identifiers
        "thisIsAReallyLongCamelCaseIdentifierThatMightAppearInCodeAndTestsTokenizerHandlingOfLongWords",
        "SCREAMING_SNAKE_CASE_CONSTANT_THAT_IS_VERY_LONG_AND_DESCRIPTIVE_OF_WHAT_IT_REPRESENTS",
        "this_is_a_very_long_snake_case_variable_name_that_exceeds_normal_identifier_length_limits",
        # IP addresses
        "192.168.100.200:8080",
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        # Version strings
        "v1.23.456-beta.7+build.20240101.abc123def",
        "python-3.12.0-linux-x86_64.tar.gz",
        # Long numbers
        "123456789012345678901234567890",
        "3.14159265358979323846264338327950288419716939937510",
        "0x00000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        "0b1010101010101010101010101010101010101010101010101010101010101010",
        "1_000_000_000_000 (with underscores)",
    ],

    "repeated_characters": [
        "a" * 100,
        "!" * 50,
        "ab" * 40,
        "☺" * 30,
        "." * 80,
        "ha" * 25 + "!",
        "Go " * 20 + "Team!",
        "Na " * 16 + "Batman!",
        "aaaaaabbbbbccccc",
        "abcdefghijklmnopqrstuvwxyz" * 3,
        "1234567890" * 5,
        "🔥" * 20,
        "test " * 50,
        "X" * 200,
        "the the the the the the the the the the",
    ],

    "emojis_and_unicode": [
        "Hello 🌍 World 🌎 Earth 🌏",
        "Emotions: 😀😂🥹😭😱🤯🥳😎🤔💀",
        "Animals: 🐶🐱🐭🐹🐰🦊🐻🐼🐨🐯🦁",
        "Food: 🍎🍊🍋🍇🍓🫐🍑🍒🥭🍍",
        "Flags: 🏴󠁧󠁢󠁥󠁮󠁧󠁿 🏴󠁧󠁢󠁳󠁣󠁴󠁿 🏴󠁧󠁢󠁷󠁬󠁳󠁿 🇺🇸 🇬🇧 🇩🇪 🇫🇷 🇯🇵",
        "Skin tones: 👍🏻👍🏼👍🏽👍🏾👍🏿",
        "ZWJ sequences: 👨‍💻 👩‍🔬 🧑‍🎨 👨‍👩‍👧‍👦",
        "Mixed: I ❤️ AI 🤖 and NLP 🧠",
        "Text with emoji in middle: Hello😊World (no space)",
        "Repeated: 🔁🔁🔁🔁🔁",
        "Math emoji: 1️⃣2️⃣3️⃣➕4️⃣5️⃣6️⃣🟰🤔",
        "Keycaps: 0️⃣1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣#️⃣*️⃣",
        "Regional indicators: 🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯",
        "Variation selectors: ♥ vs ♥️ (text vs emoji)",
        "Ancient emoji: ☯️ ☮️ ✡️ ☪️ ✝️ ☦️ 🕉️",
    ],

    "code_switching": [
        # Common code-switching patterns across languages
        "Let's debug करते हैं इस error को",
        "Je vais faire un commit et push",
        "Vamos a hacer el deployment ahora",
        "Diese API hat einen bug im timeout handling",
        "이 코드는 O(n²) complexity를 가집니다",
        "このコードはメモリリークがある",
        "هذا الكود فيه bug في الloop",
        "функция возвращает undefined вместо null",
        "Το model έχει overfitting πρόβλημα",
        "Datasetは小さすぎてoverfittingになる",
        "Le modèle est en train de s'entraîner sur le GPU",
        "Train करो model को ज़्यादा data से",
        "이 모델은 transformer architecture를 사용합니다",
        "pip install करो और फिर import करो",
        "Мы делаем fine-tuning на нашем dataset",
    ],

    "noisy_text": [
        # OCR-like noise
        "Th1s 1s n01sy t3xt w1th numb3rs r3plac1ng l3tt3rs",
        "tHiS iS aLtErNaTiNg CaSe TeXt",
        "THIS IS ALL CAPS SHOUTING TEXT",
        "this is all lower case no punctuation no capitals",
        # Missing spaces
        "thequickbrownfoxjumpsoverthelazydog",
        "artificialintelligenceistransforminghowhumansinteractwithtechnology",
        # Extra spaces
        "t h i s   h a s   s p a c e s   b e t w e e n   e a c h   c h a r a c t e r",
        # Repeated punctuation
        "Really???? Are you sure!!!! Yes... definitely.",
        "Wait... wait... wait... OK!!!",
        # Typos and misspellings
        "Teh quikc borwn fox jmups oevr teh lzay god",
        "artifical inteligence natral langauge procesing",
        # Leetspeak
        "1337 h4x0r sp34ks 1n l33t",
        "|-|3||0 //0|2|_|)",
        # Mixed noise
        "H3ll0 W0rld!!! Th1s 1s 4 t3st... R1ght???",
        "   extra    whitespace   everywhere   in   this   sentence   ",
    ],

    "mixed_scripts_single_token": [
        # Words that mix scripts or look like they should be single tokens
        "café",
        "Pokémon",
        "naïve",
        "résumé",
        "coöperate",
        "Zürich",
        "über",
        "Göttingen",
        "São Paulo",
        "Montréal",
        "Kraków",
        "Malmö",
        "Düsseldorf",
        "Zürich",
        "Łódź",
        "Reykjavík",
        "Vilniaus",
        "Čeština",
        "Ελληνικά",
        "日本語",
    ],

    "numerical_edge_cases": [
        # Various number formats
        "1,000,000",
        "1.000.000",
        "1 000 000",
        "1_000_000",
        "1e6",
        "1E+6",
        "1.5e-10",
        "∞",
        "−∞",
        "NaN",
        "0.1 + 0.2 = 0.30000000000000004",
        "1/3 = 0.333...",
        "π ≈ 3.14159265358979...",
        "e ≈ 2.71828182845904...",
        "√2 ≈ 1.41421356237309...",
        "0x1A2B3C4D",
        "0o755",
        "0b11001010",
        "1st 2nd 3rd 4th 5th 11th 12th 13th 21st 22nd",
        "½ ⅓ ¼ ⅔ ¾ ⅛ ⅜ ⅝ ⅞",
        "① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩",
        "Roman: I II III IV V VI VII VIII IX X L C D M",
    ],

    "special_punctuation": [
        # Quotes
        '"double quotes"',
        "'single quotes'",
        "\u201ccurly double\u201d",
        "\u2018curly single\u2019",
        "«guillemets»",
        "\u201elow-high quotes\u201c",
        "「Japanese」『quotes』",
        "「 」〔 〕【 】〖 〗",
        # Dashes
        "hyphen-minus: -",
        "en dash: \u2013",
        "em dash: \u2014",
        "figure dash: \u2012",
        "horizontal bar: \u2015",
        # Ellipsis
        "three dots: ...",
        "ellipsis: \u2026",
        "vertical ellipsis: \u22ee",
        # Arrows
        "→ ← ↑ ↓ ↔ ↕ ⟶ ⟵ ⇒ ⇐ ⇔",
        "➔ ➡ ⬅ ⬆ ⬇ 🔜 🔛",
        # Currency symbols
        "$ € £ ¥ ₹ ₩ ₪ ₫ ₭ ₮ ₯ ₰ ₱ ₲ ₳ ₴ ₵ ₶ ₷ ₸ ₺ ₻ ₼ ₽ ₾ ₿",
        # Misc
        "© ® ™ ℠ ℃ ℉ № ℅ ℆",
        "♠ ♣ ♥ ♦ ♤ ♧ ♡ ♢",
        "★ ☆ ✓ ✗ ✘ ✔ ✕ ✖",
    ],

    "control_characters": [
        "null: \x00 byte",
        "bell: \x07 character",
        "backspace: \x08 character",
        "escape: \x1b character",
        "delete: \x7f character",
        "unit separator: \x1f",
        "record separator: \x1e",
        # ANSI escape sequences (as they appear in terminal output)
        "\x1b[31mred text\x1b[0m",
        "\x1b[1m\x1b[32mbold green\x1b[0m",
        "\x1b[2J\x1b[H",  # clear screen
        # Unicode control characters
        "\u0000\u0001\u0002\u0003",
        "\u0085",  # next line
        "\u2028",  # line separator
        "\u2029",  # paragraph separator
        "\ufffe",  # reversed BOM
        "\uffff",  # non-character
    ],

    "fertility_test": [
        # These test subword fertility (tokens per word) across morphologically complex languages
        "türkçeleştiremeyebileceklerimizdenmişsiniz",  # Turkish: "you are reportedly one of those we could not make Turkish"
        "Rindfleischetikettierungsüberwachungsaufgabenübertragungsgesetz",  # German compound word
        "konstantynopolitańczykowianeczka",  # Polish: "little girl from Constantinople"
        "nieprzeproszonychmilionów",  # Polish
        "Hottentottenstottertrottelmutter",  # German
        "lentokonesuihkuturbiinimoottoriapumekaanikkoaliupseerioppilas",  # Finnish: "airplane jet turbine engine mechanic non-commissioned officer student"
        "Naapurinkoiran pissahaisu",  # Finnish
        "сельскохозяйственный",  # Russian: "agricultural"
        "недобросовестный",  # Russian: "unscrupulous"
        "пятисотрублёвый",  # Russian: "five-hundred-ruble"
        "কিছুতেই",  # Bengali
        "হৃদয়বিদারক",  # Bengali
        "আলোকবর্ষ",  # Bengali
        "திருவனந்தபுரத்திலிருந்து",  # Tamil: "from Thiruvananthapuram"
        "அமெரிக்காவில்",  # Tamil
        "การประมวลผลภาษาธรรมชาติ",  # Thai: NLP (no spaces)
        "คอมพิวเตอร์วิทยาศาสตร์",  # Thai: Computer Science
        "ครอบครัวของพวกเขา",  # Thai
        "人工知能自然言語処理",  # Japanese NLP
        "機械学習深層学習",  # Japanese ML/DL
    ],

    "segmentation_boundaries": [
        # Compound words that should/shouldn't split
        "cannot vs can not vs can't",
        "backup vs back up vs back-up",
        "email vs e-mail vs E-mail",
        "online vs on-line vs on line",
        "website vs web site vs web-site",
        "healthcare vs health care vs health-care",
        "database vs data base vs data-base",
        "username vs user name vs user-name",
        # Contractions
        "don't can't won't isn't aren't wasn't weren't",
        "I'm I've I'll I'd you're you've you'll you'd",
        "it's it'll that's there's what's who's",
        "they're they've they'll they'd we're we've we'll we'd",
        # Hyphenated compounds
        "well-known state-of-the-art cutting-edge",
        "two-thirds one-half three-quarters",
        "co-author pre-processing re-tokenization",
        "x-ray t-shirt e-mail",
        # Possessives
        "John's Mary's children's boss's",
        "its vs it's (possessive vs contraction)",
        "who's vs whose",
        # Abbreviations with periods
        "U.S.A. vs USA vs U.S.A",
        "e.g. i.e. etc. vs etc vs etc.",
        "Dr. Mr. Mrs. Ms. Prof. vs Dr Mr Mrs",
        "Jan. Feb. Mar. Apr. vs Jan Feb Mar",
    ],
}
