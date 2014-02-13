__author__ = 'Nitin'

from pattern.text.en import parsetree
from utils import get_tokenized_words

#Looks at PP chunks to see if certain simile words are present.
#Can be improved by checking that an adjective precedes an 'as' or 'than' simile
#  and a verb precedes a 'like' simile
def detect_simile(poem):
    full = ""

    for line in poem:
        full += line + " "

    s = parsetree(full, relations=True)

    similes = []
    simile_words = {'like', 'as', 'than', 'to'}
    for sentence in s.sentences:
        for pnp_chunk in sentence.pnp:
            words = set(pnp_chunk.string.split(" "))
            if list(words & simile_words) and valid_simile_structure(sentence.string, list(words & simile_words)):
                    similes.append(sentence.string)

    return similes


def valid_simile_structure(sentence, simile_words):

    if 'like' in simile_words:
        s = parsetree(sentence[:sentence.index('like')], relations=True)
        if s.sentences[0].verbs:
            return True

    if 'as' in simile_words:
        s = parsetree(sentence[:sentence.rfind('as')], relations=True)
        for word in s.sentences[0]:
            if word.type.startswith('J'):
                return True
    elif 'than' in simile_words:
        s = parsetree(sentence[:sentence.index('than')], relations=True)
        for word in s.sentences[0]:
            if word.type.startswith('J'):
                return True

    return False


onomatopoeia = {'argh', 'ah', 'aah', 'aha', 'ahahah', 'ah uh ah uh', 'atchoo', 'ahem', 'ahh ha ha', 'ahoy', 'arf',
                'aroo', 'aw', 'baa', 'babble', 'babbler', 'badaboom', 'bah', 'bam', 'bamf', 'bang', 'baraag', 'barf',
                'bark', 'baroom', 'bash', 'bawl', 'bay', 'beep', 'bellbird', 'biff', 'blab', 'blah', 'blam', 'blare',
                'blast', 'bleat', 'bleep', 'bling bling', 'blip', 'bllgh blllgggh blllllgggghh', 'blurp', 'blurt',
                'bobolink', 'bob-white', 'bomb', 'bomp', 'bonk', 'bong', 'boo', 'boooOOOOOOooo', 'boo-hoo', 'boom',
                'bop', 'borborygmus', 'bow-wow', 'bray', 'bratatat', '"brekekekex, koax, koax"', 'bringg', 'brouhaha',
                'bubble', 'buffet', 'buffoon', 'bumble', 'bump', 'burble', 'burp', 'burr', 'buzz', 'bwahaha!', 'bwak',
                'bweee', 'bwok', 'bwoom', 'bwow-chcka-bwow', 'bzzz', 'cackle', 'caterwaul', 'caw', 'chachalaca',
                'cha-cha-cha', 'cham', 'chat', 'chatter', 'chatterer', 'cheep', 'chickadee', 'chiffchaff', 'chiming',
                'chink', 'chirp', 'chirr', 'chirrup', 'chit-chat', 'chitter', 'chomp', 'choo-choo', 'chortle', 'chough',
                "chuck-will's-widow", 'chug', 'chunk', 'clack', 'clackety-clack', 'clang', 'clank', 'clap', 'claque',
                'clash', 'clatter', 'cliche', 'click', 'clickety-clack', 'clink', 'clinker', 'clip clop',
                'clippity-clop', 'clitter', 'clobber', 'cltkty', 'cluck', 'cock-a-doodle-doo', 'common poor-will',
                'coo', 'cough', 'crack', 'crash', 'creak', 'cricket', 'crinkle', 'croak', 'croup', 'crow', 'crunch',
                'cry', 'cuckcoo', 'curlew', 'currawong', 'dab', 'dada', 'dash', 'deed-a-reedle',
                'dibble dibble dopp dopp', 'dickcissel', 'didgeridoo', 'ding', 'ding-dong', "d'oh", 'dong', 'doo-wop',
                'dook', 'dot a dot dot', 'drone', 'duh', 'eastern phoebe', 'eastern whipbird', 'eee-aaaah', 'eeeeeee',
                'eeeoooeeeooo', 'eek eek', 'eeeyouch', 'eh', 'fanfare', 'fap fap fap', 'fart', 'fash', 'fillip',
                'finch', 'fizz', 'flap', 'flash', 'flatulence', 'flick', 'flick a flack fleck', 'flicker', 'flip-flop',
                'flog', 'flop', 'flutter', '"freh, freh, freh"', 'frou-frou', 'gabing', '"gada, gada, gada"', 'gag',
                'gaggle', 'gargle', 'gasp', 'gecko', 'gibberish', 'giggle', 'glok', 'glop', 'glug', 'gnash', 'gnaw',
                'gobble', 'gong', 'gray-winged trumpeter', 'great kiskadee', 'groan', 'growl', 'grumble', 'grump',
                'grunt', 'guffaw', 'gulp', '"gunko, gunko"', 'gurgle', '"gwuf, gwuf, gwuf"', '"gyuh gyuh,gyuh"', 'ha.',
                'ha!', 'ha ha', 'ha-ha-ha-HA-ha', 'HA-ha!', 'hackigi-gi-gi-gi', 'hah!', 'har har!', 'haw', 'hee!',
                'hee haw', 'he-he', '"heh, heh!"', 'hehehe!', 'hem', 'hey', 'hi', 'hiccup', 'hip', 'hiss',
                'hissssssssss ssss ss', 'hm', 'hmpf', 'ho ho ho!', 'hohn hohn hohn hohn', 'ho hum', 'hawk', 'honk',
                'hoo hoo', 'hoo hoo hoo hoo', 'hoopoe', 'hooray', 'hoot', 'hottentot', 'howl', 'hrrooonnh', 'huff',
                'huh', 'huh huh huh', 'hum', 'humph', 'hurrah', 'hush', 'huuuooohar', 'huuuuuuuuuugh ', 'hyuk hyuk',
                'jabber', 'jar', 'jangle', 'jee je je jeee', 'jingle', 'jug', 'jump', 'kaboom', 'ka-ching', 'kapow',
                'kashl', 'kata-kata', 'katydid', 'kea', 'kekekeke', 'killdeer', 'kirik', 'kite', 'kittiwake', 'klam',
                'klok', 'klopp klopp klopp', 'klunk', 'knack', 'knell', 'knock-knock', 'knot', 'koink', 'kong',
                '"kra, ka, ka, hi"', 'kut-kut-kut', 'kwok', 'lap', 'lash', 'lilt', 'lisp', 'low', 'meow', 'mew', 'moan',
                'moo', 'mopoke', 'morepork', 'mrow', 'mrrrrgggggllll', 'mum', 'mumble', 'munch', 'murmur', 'muuhhhrrr',
                'mutter', 'mwahaha', '"na na, na NA na"', 'naa', 'natter', '"neener, neener"', 'neigh', 'neow',
                'northern flicker', '"nyah, nyah"', 'oink', 'om nom nom', 'oo oo oo', 'oooaughoaua', 'ooh', 'ook',
                'oompah', 'oops', 'ouch', 'ow', 'owooooah', 'pad', 'pah-pa-rah', 'pat', 'patter', 'pee-oo-wee',
                'peeper', 'pew pew', 'pewee', 'pewit', 'phew', 'phoebe', 'phooey', 'pickle-pee', 'pied currawong',
                'ping ', 'ping-pong', 'pip', 'pitter-patter', 'plain chachalaca', 'plonk', 'plop', 'plump', 'plunk',
                'pop', 'pow', 'prrr', 'psst', 'ptooey', 'puh-puh-puh', 'puke', 'pump', 'pump-a-rum', 'punt', 'purr',
                'quack', 'rabble', 'racket', 'rail', 'rap', 'raspberry', 'rataplan', 'ratatatat', 'rattle', 'red knot',
                'reek', 'ribbit', 'rinky-dink', 'roar', 'rooaaarrr', 'rowr', 'rub-a-dub', 'rumble', 'rustle',
                'rrrruuuurrrr', 'schlip', 'scratch', 'scream', 'screamer', 'screech', 'scritch', 'scrunch', 'shashing',
                'shiiiiing', 'shiiin', 'shoo', 'shoop', 'shriek', '"shuh, shuh, shuh"', 'shush', 'shwap', 'sigh',
                'siss', 'sizzle', 'skirl', 'skraww', 'skreek', 'slam', 'slap', 'slobber', 'slosh', 'slump', 'slurp',
                'smack', 'snap', 'snarl', 'sneeze', 'snicker', 'sniff', 'sniffle', 'snikt', 'snip', 'snore', 'snort',
                'sob', 'sora', 'spack a speck speck', 'splash', 'splat', 'splatt', 'splatter', 'splosh', 'splut',
                'spoing', 'spoot', 'sputter', 'squabble', 'squall', 'squawk', 'squeak', 'squeal', 'squirt', 'squish',
                'sssshblamm', 'strident', 'strum', 'stup', 'suru suru', 'susurration', 'swah', 'swash', 'swish ',
                'swoosh', 'ta-da', 'takka takka', 'tap', 'tattle', "t'chi", '"tch, tch, tch"', 'teehee!',
                'terwit terwoo', 'throb', 'thrum', 'thubalup', 'thud', 'thump', 'thung', 'thunk', 'thwack', 'thwogg',
                'thwip', 'tick', 'tick tock', 'tintinnabulation', 'tinkle', 'tinkling', 'titter', 'tlick', 'tolling',
                'tom-tom', 'toot', 'tootle-too', 'trill', 'trumpeter', 'tu-whu', 'tup', 'twang', 'tweet', 'tweeter',
                'twiddle', 'twit twoo', 'twitter', 'tzing', 'uggh', 'ugh', 'uh-huh', 'uh-oh', 'umpa', 'untz untz untz',
                'varoom', 'veery', 'viip', 'voomp', 'vroom', 'vzzzzt', 'waak', 'wah-wah', 'wahoo', 'wallop', 'wap',
                'weeeoooeee', 'weep', 'whaam', 'whack', 'wham', 'whang', 'whap', 'whee', 'wheeze', 'whew', 'whiff',
                'whimper', 'whine', 'whinny', 'whipbird', 'whip-poor-will', 'whirr', 'whish', 'whisper', 'whistle',
                'whit woo', 'whizz', 'whoa', 'whock', 'whockah', 'whomp', 'whoop', 'whoops', 'whooping crane',
                'whooping cough', 'woops', 'whoosh', 'whop', 'whump', 'willet', '"woah, oh, oh, oh!"',
                'woh woh woh woh', 'woo-woo-woo', 'woo-hoo!', 'wow', 'wuh-uh-uh-uh', 'yadda yadda', 'yahoo', 'yammer',
                'yar', 'yawp', 'yay', '"yeeha, yeehaw, yee-haw"', 'yelp', 'yeow', 'yip', 'yippee', 'yodel', 'yoink',
                'yoo-hoo', 'yoooo', 'yowl', 'yowt', 'yucchh', 'yuck', 'yuk yuk', 'yummy', 'zap', 'zing', 'zip', 'zonk',
                'zoom', 'zoomba-zoom', 'zzzz', 'tuckaTHUCKtuckaTHUCKtucka', '"vooRRRR, vooRRR, vooRRR"',
                'YEEeeEEeeEEeeEEeeEEee!', '"floovb, floovb, vwomp, vwomp"', 'bwwob bwwwobbubwub',
                'puhVRooPuhHoo puhVROOpuhHOO', 'nnnghuh nnnguh', 'vroo-vroo', 'vreeeeeeeeeeeeeeew', 'poomb',
                'Ffffffffffffff', 'Kaaahhkkk', 'Krrrrrrrr', 'gak', 'argh', 'awk', 'aaht aahht bloooot', 'badonkadonk',
                'dodogyuuun', 'chukar', 'dikdik', 'hummingbird', 'bumblebee', 'rattlesnake',
                '"chumma chumma chumma, hufft hufft, falump"', 'howler monkey', 'croaker', 'tuk-tuk', 'schlikt',
                'vworp', 'crackle', 'houyhnhnm', 'poof', 'yikes', 'tsk', 'flush', 'squelch', 'badum tish', 'tlot tlot',
                'croon', 'moob', 'cha-ching', 'gurrhr', 'mkgnao', 'boff', 'zlopp', 'sock', 'aaugh', 'fa-thud', 'p-taff',
                '"gulla, gulla, glugluglugluglug"', 'tuff', 'schhwaff', 'flumppf', 'dwoiiinnnnnnnngggggggig', 'shazam',
                ' ca-chunk', 'thwok', 'nnneeaoowww', 'kish-kish', 'pap', 'fwww - cluck', 'hhhhrrrrrrnnnnngggg', 'blop',
                'piaaaak', 'kaaapooooom', 'thisshig rrrerrk', '"shuush, shuush"', '"ssinda, sssssinda"', 'yakyakyakyak',
                'Plip - plip - ploop - plip - plip - plip - plip - ploop', 'tk.tk.tk.tk.tk.tk',
                'schwump schwump schwump schwump', 'skrrreeek', 'penk', 'waaank', 'rizzz', 'zchunk',
                'BWEEP bip bip BWEEP', 'NEE-eu NEE-eu', 'flibbertigibbet', 'yackety-yak', 'dakka', 'breet',
                'whop whop whop', 'wuppa wuppa', 'whumpa-whumpa-whumpa-whumpa', 'whup-whup-whup', 'flac-flac-flac',
                '"chakk-chackk-chak-chak, chak-a-chak-akk-chk-chk-chk"', 'dubdubdubdubdubdub', 'thith-thith-thith',
                'batabatabata', 'tocotocotoco', 'harumph', 'skraaa', 'wakt', 'throkk', 'ah-ooh-ga', 'wub wub', 'oonse',
                'dirnt', 'pht', '"crunch, crunch, crunch"', '"shuffle, shuffle, shuffle"', '"tack, tack, tack"',
                '"wher, wher, wher"', 'brum-brum-brum-brum-brrrrrrrrrrrrrrrrrrrrr', 'Fnarr! Fnarr!',
                'wlu-wlu-wlu-wlu-wlu-wlu-wlu', 'boosh', 'Whargharble', 'potato-potato-potato', '"Schklikt, klikt"',
                'Chrrrick chrrrick chrrrick chrrrrick', 'tabdak tabdak', 'bum! brrum! brrrumble!!!!', 'fwappa',
                'ow-wow-wow-wow', 'ack-ack-ack-ackawoooo-ack-ack-ack', 'squirm', 'squiggle', 'plink',
                'shlick shlick shlick', 'tluck....tlock', 'Tlick - Tlock Tlick - Tlock',
                'Tluuck tluck tlawck tlock tlaack tlack tlick!', 'gobbledygook', 'guff',
                'grrrakka kkakkakkakkakkakkakk akkakkakk kkakka akk', 'gr gr k k grk',
                'beep beep beep beep beep beep whirrrffftt bonk', 'kookaburra', 'oomph', 'lub-dub-lub-dub-lub-dub ...',
                'beep beep beep beep screeeech ruuurrrump pa-lump', 'gshaaaa', 'skwee brrumm brrumm skoooooo skooooo',
                'poop', 'owl', 'marauder', 'chug chugchug chugchug mmmoooosh', 'bazinga', 'grrrraaawr', 'hu hu hu hu',
                'brinng', 'hah-hah-hah', 'heh-heh-heh', 'ah-choo', 'achoo', 'woof', 'ruff', 'blabber', 'yap', 'sheesh',
                'geez', 'pock', 'thong-thong', 'ching-a-ling', 'brahnk', 'champ', 'woop woop', 'wak wak ',
                'fwip fwip fwip', 'kerfuffle', 'mrrroww', 'nnn...nnn...nnn', 'ar rooff', 'rrowff', 'raow'}


def identify_onomatopoeia(poem):
    words = []
    for line in poem:
        words.extend(get_tokenized_words(line))

    return list(set(words) & onomatopoeia)

