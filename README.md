Your submission does not fulfill the standards to pass this assignment yet. You will be given a chance to fix the named issues in a week's time from now on, which means until June 19th, 2024. For simplicity, we recommend that you include your fixes in your submission for PR03 and submit it all together. If your submission for PR03 also passes all requirements from PR02, we will update your evaluation here.

The following feedback was given by the evaluator. Please use this to address the issues in your code:
- create_stop_word_list_by_frequency returns too little stop words for the given documents. Please review the code.
- Your query representation seems to be something else than list or set. Keep in mind that in the Boolean model, representations are sets of str (even if they only have 1 element).
- There might be an issue with your matching function. Some of our tests with it failed, so please review it and run some more of your own tests.
