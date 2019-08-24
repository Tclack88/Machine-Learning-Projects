# Naive Bayes Spam Filter

This is my attempt to redo an assigned school project, but much better rather than following a "cookie-cutter" task list, I thought I'd do it from scratch but using ML libraries when convenient. You can read about it in my blog here: [spam filter](https://tclack88.github.io/blog/code/2019/07/01/spamfilter.html)

## Content
`spam.tar.gz`<br>
This tar file contains all the spam/non-spam files

`train.list` and `test.list`<br>
text files containing the location of the train, test data. This could of course be automated with sklearn's `split_train_test` method, but I was working off the problem as given originally where the data was pre-chosen.

`make_spam_model.py`<br>
This is the main function. It requies 2 files: `train.list` and `test.list` and the corresponding directory with the spam samples. The train and test lists are hard-coded in the code

`NBfunc.py`<br>
Support functions for `make_spam_model.py` and `test_spam_model.py`

`cleanup.sh`<br>
An optional shell script which will clean all files of non-ascii bytes. If `make_spam_model.py` runs without error, this sholdn't be necessary

`test_spam_model.py`<br>
An additional python script I wrote which can be called on either a file (.txt) or a directory containing multiple files. It will return which of them are spam and not spam. Have fun with this!

`spamkeys.py`<br>
This gets created when `make_spam_model.py` is run, it's a set of keys which save time so the text files don't need to be re-read and words recounted before running `test_spam_model.py`

`spam_model.sav`<br>
This is just the python pickle file which saves the model after running `make_spam_model.py`. Again the purpose of this is so it doesn't take several minutes to determine if a single text file is spam or not

## How to Use
If you want to just use the model to test spam, just download: `NBfunc.py`, `spam_keys.py`, \*`spam_model.sav`, and `test_spam_model.py` then you simply call it on a text file or directory of your choice: eg. `test_spam_model.py is_it_spam.txt`

If you want to create a predictive model using your own samples, consider making a train/test list (you can segment off random choices from one master directory using a simple bash script) then download: `NBfunc.py`, `make_spam_model.py`, `cleanup.sh`(optional). You will need to change the hardcoded values for the variables "train\_data" and "test\_data" if you decide not to use `valid.list` and `train.list` as your title. Optinally you can change the name of the save file in the "outfile" variable, but you would also need to make the corresponding change in the `test_spam_filter.py` script as well.

* It's a pickle file, [do you trust me](https://www.synopsys.com/blogs/software-security/python-pickling/)?
> "Since there are no effective ways to verify the pickle stream being unpickled, it is possible to provide malicious shell code as input, causing remote code execution. The most common attack scenario leading to this would be to trust raw pickle data received over the network."

