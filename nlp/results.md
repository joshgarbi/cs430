# Names: Josh Bielas and Josh Garbi
# Lab: lab6 (NLP)
# Date: 3/4/2026

1. Looking at the attention matrix for layer 1, head 1, which token receives the most attention from the word "it"? Does this match your linguistic intuition about what "it" should refer to in the sentence? Why or why not?

    The word that receives the most attention from the word "it" is the word "is". This does not match our linguistic intuition because "it" should refer to a noun. Intuitive relationships don't always appear how they should in every layer of every head.


2. The [CLS] token often accumulates disproportionately high attention. What role does [CLS] play in BERT's architecture, and why might many tokens attend strongly to it even though it carries no dictionary meaning?

    The [CLS] token stores information from the whole sentence as sort of a summary. Many tokens attend strognly to it even though it carries no dictionary meaning because it has information about the whole input, so all tokens would attend to it. It ends up working as a key for the sentence because it has information about all of it. We did some research here: https://aditya007.medium.com/understanding-the-cls-token-in-bert-a-comprehensive-guide-a62b3b94a941

3. Attention is sometimes described as a "soft lookup" — rather than retrieving one fixed answer, the model blends information from many tokens weighted by relevance. How does this differ from how a traditional rule-based parser would resolve pronoun reference?

    It resolves pronoun references based on probability distributions instead of a guaranteed rule. This is better because in natural language certain procedures might be broken in other cases. It can be very hard to always know how two tokens will interact. It allows us to follow the correctness of a language that is hard to define by a set of rules.

4. After exploring multiple heads in layer 1, describe two heads that appear to capture qualitatively different relationships. What linguistic patterns do you think each is tracking, and what evidence in the visualization supports your interpretation?

    2nd Head seems to show relationships between neighboring words in the sentence. the 4th Head is much different with a wider variation and very few coorilations between neighboring words. the 2nd head might be capturing local syntax structure from one word to the next while the head 4 is targeting more distance syntax relationships.

5. Compare the overall "texture" of attention in layer 1 vs. layer 8 vs. layer 12. In which layer do attention patterns look more diffuse (spread across many tokens) vs. more focused? What might this difference tell us about the progression from syntactic to semantic processing?

    the higher heads seem to have more focused patterns that seem directed and cleaner. The important relationships become more apparent when the model progresses towards semantic processing from syntactic processing.

6. The AIMA book describes intelligence as the ability to act appropriately given incomplete information. In what sense does multi-head attention allow a model to handle ambiguity — like the ambiguous "it" in our sentence — better than a single attention head would?

    The more attention heads allows the model to consider more types of relationships. The result of considering different types of realative patterns is that it can diminish ambiguity and reveal patterns/answers.

7. In layer 12, does "it" consistently attend more to "trophy" than "suitcase" across all heads? Are there heads where "suitcase" dominates? What does this variability across heads suggest about how BERT distributes reasoning across its components?

    Yes, most heads show more attention to from "it" to "trophy", there are a few heads that have a higher attention towards "suitcase". heads with higher attention carry more weight towards the prefferd reference. The chart shows heads with the highest attention value attending "it" much more. 

8. Attention weight alone does not prove a model has "understood" coreference — it is a correlation, not a causal explanation. What additional experiment could you design to test whether BERT truly resolves this Winograd Schema correctly?

    you could rearrange the sentence so that while it may not make sence to a enlgish reader, the rearanged text while test BERT's ability to reliably reproduce coorilation between syntax structure vs semantic structure. 

9. The Winograd Schema was proposed as a test of machine intelligence that is trivial for humans but hard for simple statistical models. Based on what you've observed in these attention exercises, do you think BERT "understands" this sentence in a meaningful sense? Defend your position using specific observations from the lab.

    Yes, Bert correctly determined the semantic relationship between "it" and "trophy" vs "suitcase". In the case where the sentence was rearanged to say: "The suitcase trophy doesn't fit in the because it is too big.". while the sentence doesnt make sense to us, BERT was still able to identify "it" to "Trophy" even though the sentence attempted to break its process from before.

10. Describe the spatial organization of the three word clusters in your plot. Are they clearly separated, or do any categories overlap? Which two categories are most geometrically similar to each other, and why might that be?

    The groups are distantly separated. Animals seem to be closer to professions than countries, this may be because the professions relate to humans which are a living being in that sense, while countries are a location. In sentence structure its more likely that a animal noun and a profession noun are used interchangably compared to countries.

11. The distributional hypothesis underpins word embeddings: words are similar if they appear in similar contexts. Can you think of a pair of words that would be incorrectly placed near each other by this principle (false semantic neighbor), or a pair incorrectly placed far apart (false semantic distance)? What does this suggest about the limits of corpus-based meaning?

    In the graph Egypt and Mexico are close than any other pair in any other group. The model thinks that they are very interchangable, but in reality it shouldn't be more than other countries in the list. Additionaly, sentences that begin with "He saw..." for example, have many possible nouns to fill in but adding adjectives like a color or "fast" would eliminate possible words.

12. For the analogy man:king :: woman:?, did the model return "queen" as the top answer? Look at the full top-5 list — are the other answers plausible or surprising? What does this tell you about what the model has actually learned vs. what we might hope it learns?

    Yes, some of the other answers for that prompt seem reasonable and also follow identifiable logic. although, "throne" is an object that the model probably derived from "King" but wasnt considered against the relationship with "man". "monarch" as #2 is interesting because it's not a gender specific role like king vs queen. the following answers also follow the same logic as "queen"
    in the 2nd attempt the model got the correct answer and since there is only one logical response it seemed to fill in related or possible common wrong guesses.
    the last one is interesting because the correct answer was #3 instead of #1. the other words relate but dont follow the correct English logic.

13. In the bias probe, which professions are most strongly associated with "man," and which with "woman"? Do these associations reflect linguistic reality (how these words actually co-occur in text) or social stereotypes — or both? Why is it difficult to separate the two?

    Nurse and Doctor are more strongly associated with "woman" while ceo and engineer are more strongly associated with "man". These associations do reflect linguistic reality. Text and stereotypes are difficult to separate because stereotypes often come about from text, content and aren't as easily quantifiable in the same way as the titles apear in text.

14. List the three tokens with the highest saliency scores. Are they the words you would intuitively consider most important for determining sentiment? If there are surprises (e.g., punctuation or function words scoring high), propose a hypothesis for why the model might be sensitive to them.

    1. Disaster
    2. brilliant
    3. .

    the film was the topic of the sentence but didnt get a saliency that was very high. the period at the end of the sentece scored #3. The model might be sensitive to punctuation because it marks the end of semantic and syntax analysis in other words the model is always looking for punctuation to understand the end of the analysis. 

15. This sentence contains both positive ("brilliant") and negative ("disaster") sentiment words. Which scores higher in saliency? What does this tell you about how the model balances conflicting sentiment signals, and does it match the model's final prediction?

    disaster was considerably higher (over 2x). This means that the model is heavily swayed by negative sentiment over positive. It means that the model will predict negative outcomes more confidently when a negative adjective is apparent. It does match the prediction

16. Which masked word caused the largest drop in confidence? Did any masking cause the predicted label to flip? What do these results tell you about the relative causal importance of different tokens compared to what saliency scores alone predicted?

    Disaster cause the largest drop in confidence. Masking disaster also caused the prediction label to flip from negative to positive. This shows that just having one negative token can change the label of the entire sentence eve if there are more than 1 positive tokens as well.

17. Masking "was" likely had little effect on the prediction, yet some function words may have had non-trivial saliency scores in Exercise 6. How do you reconcile these two findings? What does this suggest about the difference between gradient sensitivity and causal importance?

    Just because a word/token has a relatively high saliency value does not always mean that its mask will change the prediction. Apart from saliency, tokens/words relate to other tokens in a probability distribution. A word may have a higher saliency but not change the sentiment when masked.

18. For the pairs where adding or removing "not" changes the label, is the confidence shift large or small compared to swapping a positive word for a negative one (e.g., "excellent" → "terrible")? What does the relative magnitude of these confidence changes reveal about how the model weights negation versus lexical sentiment signal?

    It is smaller than changing the positive word. The model takes more notice in lexical sentiment than negation. changing a word/meaning is more vital than adding a positive/negative modifier to a word.

19. The pair "She gave a brilliant performance." vs. "She gave a performance." removes the adjective entirely. Does the model's prediction change meaningfully? What does this reveal about whether the model is classifying based on the presence of sentiment-bearing adjectives or on a more holistic sentence-level representation?

    The prediction didnt change with the removal of brilliant. this suggests that the model takes a sentence level aproach when identifying sentiment. The sentence is just as positive with no negative words than with one positive word.
