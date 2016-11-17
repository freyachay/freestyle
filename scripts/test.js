// *********** CLASSES ***********
// ## Syl
// Syls are the main elements used to structure our rhyme comparison.
// Syls map to syllables and are compared to other syllables to establish rhyme.
function Syl(sounds,index,pro_index){
    this.sounds = sounds;
    this.raw_sounds = _.map(sounds,function(s){
        return destress(s);
    });
    
    // We break the syllable into a vowel, a prefix, and a suffix.
    this.vowel = _.find(sounds,function(s){
        return _.contains(vowel_sounds,destress(s));
    });

    this.vowel_index = sounds.indexOf(this.vowel);
    this.suffix = sounds.slice(this.vowel_index + 1);
    this.prefix = this.sounds.slice(0,this.vowel_index);

    // Syllable index and pronunciation index are use for contextual comparisons with
    // other syllables based on position
    this.index = index;
    this.pro_index = pro_index;

    // Total mark will record how strongly the syllable rhymes with all other syllables
    // in the verse
    this.total_mark = 0;

    // Color is used to group syllables into rhyme families
    this.color = 0;

    // Stress is used to score the quality of rhymes. Two stressed syllables rhyme more
    // strongly than one stressed and one unstressed. One stressed and one unstressed 
    // syllable rhyme more strongly than two unstressed syllables.
    if(! this.vowel){
        this.stressed = false;
    } else {
        this.stressed = this.vowel.indexOf("1") > 0 || this.vowel.indexOf("2") > 0;
    }

    // Head and tail neighbors are used to form rhyme patterns and strengthen or weaken
    // rhyme scores based on nearness to other rhyming syllables
    this.head_neighbors = [];
    this.tail_neighbors = [];

    // End word determines if the syllable is part of the last word on a line.
    // This is used to identify end rhymes.
    this.end_word = false;

}

// The label function is used to generate unique ids for each syllable, which 
// will be used for node names in the eventual syllable graph
Syl.prototype.label = function(){
    return this.parent.index + "-" + this.index + "-" + this.pro_index;
};

// The sameAs function is used to evaluate similar syllables across pronunciations
Syl.prototype.sameAs = function(s){
    return this.index == s.index &&
           this.parent.index == s.parent.index;
};

// ## Phoword
// Syllables are collected into pronuncation arrays, collected into Phowords. This 
// allows us to eventually map the syllables back onto the original words.
function Phoword(word,pros,index){
    this.word = word;
    this.pros = pros;
    this.index = index;
    this.sentence = -1;
    this.final_syls = [];

    var w = this;

    // For the last Phoword of each line, mark each of their syllables as belonging
    // to an end word.
    _.each(pros,function(p){
        var last_syl = p.length - 1;
        _.each(p,function(syl,i){
            syl.parent = w;
            if(i == last_syl){
                syl.end_syl = true;
            } else {
                syl.end_syl = false;
            }
        });
    });
}
// ********************************


// ********* FUNCTIONS ************
// **cleanSentence**
//
// Remove all smart apostrophes and single quotes
function cleanSentence(sentence){
    return _.map(sentence,function(word){
        return word.replace(/â€™|â€˜/g,"'");
    });
}

// **replacePros**
//
// Used to manually adjust certain pronuncations 
function replacePros(word,new_sounds,last_syl){
    _.each(word.pros,function(p,pi){
        var newsyl = new Syl(new_sounds,last_syl.index,pi);
        newsyl.parent = last_syl.parent;
        p.pop();
        p.push(newsyl);
    });
    return word;
}

// **lookup**
//
// Used to translate a raw english word into a series of syllablized, arpabet
// pronunciations
function lookup(w,sentence,index){
    var pros, sylpros, final_word, new_word, word, last_syl, new_sounds, newpro;

    // You can't look the word 'constructor' up in javascript. It is a reserved word.
    if (w === "constructor"){
        pros = [["K AH0 N","S T R AH1 K","T ER0"]];
    // First, check our hand-written dictionary
    } else if(ejdict[w]){
        pros = [ejdict[w]];
    // If the word matches a multiple pronunciation entry, grab both pronuncations
    } else if (syldict[w+"(2)"]){
        pros = [syldict[w],syldict[w+"(2)"]];
    // If the word matches a single pronunciation entry, grab it
    } else if (syldict[w]){
        pros = [syldict[w]];
    // If the word ends in 'ah', try the word as an 'er' word. This is used to 
    // handle alternative pronunciation of words common in rap lyrics
    } else if (w.match(/\w+?ah$/i)){
        new_word =  w.match(/(\w+?)ah/)[1] + "er";
        word = lookup(new_word,sentence,index);

        if(word && word.pros[0]){
            last_syl = word.pros[0].slice(-1)[0];
            new_sounds = last_syl.sounds.slice(0,last_syl.vowel_index);
            new_sounds = new_sounds.concat(["AH0"]);

            replacePros(word,new_sounds,last_syl);
        }
        word.word = w;
        return word;
    // If the word ends in n', try the word as an "ng" word
    } else if (w.match(/\w+?n[\'|â€™]?$/)){
        new_word =  w.match(/\w+/)[0] + "g";
        word = lookup(new_word,sentence,index);

        if(word && word.pros[0]){
            last_syl = word.pros[0].slice(-1)[0];
            new_sounds = last_syl.sounds;
            new_sounds = new_sounds.slice(0,-1).concat(["N"]);

            replacePros(word,new_sounds,last_syl);
        }
        word.word = w;
        return word;
    // If the word ends in s', try the word without the final apostrophe
    } else if (w.match(/\w+?s[\'|â€™]$/)){
        new_word = w.match(/\w+/)[0];
        word = lookup(new_word,sentence,index);

        if(word && word.pros[0]){
            last_syl = word.pros[0].slice(-1)[0];
            new_sounds = last_syl.sounds;

            replacePros(word,new_sounds,last_syl);
        }
        word.word = w;
        return word;
    // If the word is an 's possessive, try to lookup the word without the s and then add
    // the sound back on
    } else if (w.match(/\w+\'s/)){
        new_word = w.match(/\w+/)[0];
        word = lookup(new_word,sentence,index);

        if(word && word.pros[0]){
            last_syl = word.pros[0].slice(-1)[0];
            new_sounds = last_syl.sounds;
            new_sounds = new_sounds.concat(["S"]);

            replacePros(word,new_sounds,last_syl);
        }
        word.word = w;
        return word;
    // If the word is a plural, try the word without the s and then add the sound
    // back on 
    } else if (w.match(/'\w+?s/)){
        new_word = w.replace(/s$/,"");
        word = lookup(new_word,sentence,index);

        if(word && word.pros[0]){
            last_syl = word.pros[0].slice(-1);
            new_sounds = last_syl.sounds;
            new_sounds = new_sounds.slice(0,-1).concat(["S"]);

            replacePros(word,new_sounds,last_syl);
        }
        word.word = w;
        return word;
    // Otherwise, we cannot lookup the word
    } else {
        pros = [];
        console.log("Could not lookup",w);
    }

    // Often "-shan" words such as "Egyptian" are pronounced as "-shin" words,
    // so add that pronunciation
    var er_fudge = false;
    if (pros.length === 1 && pros[0].slice(-1) && pros[0].slice(-1)[0] === "SH AH0 N"){
        newpro = _.clone(pros[0]);
        last_syl = newpro.pop();
        last_syl = "SH IH0 N";
        newpro.push(last_syl);
        pros.push(newpro);
    }

    // Often "-er" words such as "monster are pronounced as "-ah" words ("monstah"),
    // so add that pronunciation
    if (pros.length > 0 && pros[0].slice(-1) && pros[0].slice(-1)[0].match(/ER\d$/)){
        newpro = _.clone(pros[0]);
        last_syl = newpro.pop();
        last_syl = last_syl.replace(/(.*?)ER(\d)$/,"$1AH$2");
        newpro.push(last_syl);
        pros.push(newpro);
        er_fudge = true;
    }

    // Often "-ers" words such as "monster are pronounced as "-ahs" words ("monstahs"),
    // so add that pronunciation
    if (pros.length > 0 && pros[0].slice(-1) && pros[0].slice(-1)[0].match(/ER\d Z$/)){
        newpro = _.clone(pros[0]);
        last_syl = newpro.pop();
        last_syl = last_syl.replace(/(.*?)ER(\d) Z$/,"$1AH$2 Z");
        newpro.push(last_syl);
        pros.push(newpro);
        er_fudge = true;
    }

    // Map every pronunciation on to an array of Syls
    sylpros = _.map(pros, function(p,pi){
        return _.map(p, function(syl,syli){
            if(!syl){
                console.log(w);
            }
            return new Syl(syl.split(" "),syli,pi);
        });
    });

    // If we added an "-er" to "-ah" pronunciation, mark the syllable. We will
    // use this information to make rhymes against this pronunciation stricter
    if(er_fudge){
        if(sylpros.slice(-1)[0] && sylpros.slice(-1)[0].slice(-1)[0]){
            sylpros.slice(-1)[0].slice(-1)[0].er_fudge = true;
        }
    }

    final_word = new Phoword(w,sylpros,index);
    final_word.sentence = sentence;
    return final_word;
}

// **processText**
//
// Transform an array of string arrays (a series of sentences) into
// an array of Phoword arrays
function processText(text){
    var lines, filtered, numbered, index, sounds, all_words, all_syls;

    // Tokenize each line into words, separating out all non-apostrophe punctuation
    lines = _.map(text,function(line){
        return line.match(/[\w\'â€™]+|[^\w\s\'â€™]+/g);
    });

    // Remove all smart single-quotes
    lines = _.map(lines,function(s){
        return cleanSentence(s);
    });

    // Remove all non-apostrophe punctuation and other non-word noise
    filtered = _.map(lines,function(sentence){
        var words = _.filter(sentence,function(w){
            return w.match(/[\w\']{2,}|\w+/);
        });
        return _.map(words,function(w){return w.toLowerCase();});
    });

    numbered = [];
    index = 0;

    // Number each sentence and word
    _.each(filtered,function(sentence){
        var s = [];
        _.each(sentence,function(word){
            s.push([word,index]);
            index++;
        });
        numbered.push(s);
    });

    // Lookup each word and transform it into a Phoword
    sounds = _.map(numbered, function(sentence,sentence_index){
        return _.map(sentence, function(s){
            var w = s[0],
                w_index = s[1];
            return lookup(w,sentence_index,w_index);
        });
    });

    // Flatten the sentences into an array of words
    all_words = _.flatten(sounds,true);

    // Filter out any falsy values (nulls, undefineds, etc)
    all_words = _.filter(all_words,function(w){return w;});

    all_syls = [];

    // Create a flat list of syllables
    _.each(all_words,function(word){
        _.each(word.pros,function(p){
            _.each(p,function(syl){
                all_syls.push(p);
            });
        });
    });

    return [sounds,all_syls,all_words];
}
// *******************************



// ********* MAIN AREA ***********
var lyrics = document.getElementById("lyrics").innerHTML.split("\n"),
    process = processText(lyrics.concat(["xxx"])),
    sounds = process[0],
    syllables = _.flatten(process[1]),
    words = process[2];

console.log("Made it through")


// *******************************

// // Determine if any words couldn't be looked up
// var missing_words = _.some(words,function(w){
//     return w.pros.length === 0 && w.word != "xxx";
// });

// // Adjust for a strictness parameter
// mcl_param = document.getElementById("fader").value;
// window.SCALE = (mcl_param - 2)/3.5;

// // Put each syllable into a dictionary based on its label for easy
// // debugging and crossreference
// syl_dict = {};
// _.each(syllables,function(s,i){
//     syl_dict[s.label()] = s;
// });

// // Assign each syllables its neighbors
// findNeighbors(words);

// // Assign each syllables its scored rhymes
// var G = findMatches(words);

// // Pick which pronunciations to use
// var winners = pickWinners(sounds),
//     reduced_syls = winners[0],
//     flat_syls = winners[1];

// // Run our first clustering into rhyme families
// var first_mcl = createMCL(flat_syls,G,2 + SCALE);
// var partition = makeClusters(syl_dict,G,first_mcl);
// clusterColor(partition);
// var groups = cleanFinalColors(flat_syls,G,syl_dict);

// var final_mcl,final_partition,final_groups;