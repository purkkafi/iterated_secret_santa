# Iterated secret santa

A Secret Santa randomizer ideal for multiple rounds; avoids repeating giver–reciever-pairs if possible.

## Usage

Invoke the script with
a) a .csv file containing the participants and information about gifts already given (check the example)
b) the list of people present for this round (can be everybody or a subset)

For example, you can randomize a round using the example file with

`./iterated_secret_santa.py example.csv Sam,Nik,Murdoch,William,Cliff`

printing a result such as

``Sam -> Cliff
Nik -> Murdoch
Murdoch -> William
William -> Nik
Cliff -> Sam``

which indicates that Sam should give a gift to Cliff, Nik to Murdoch and so on.

**Note:** I guess you need to pass this data to a third person if you are yourself involved and don't want any spoilers. You could plausibly automate sending everybody their info, but it having somebody check that the result makes sense doesn't hurt.

## .csv file format

To enable it to randomize multiple rounds in an ideal way, the program requires a .csv file with data about gifts given on previous rounds.

Let's check the example file:


           ,Sam,Nik,Murdoch,William,Cliff
    Sam,    ---,  1,      2,      1,    1
    Nik,      2,---,      1,      1,     
    Murdoch,  1,  2,    ---,      1,     
    William,  2,  1,       ,    ---,    1
    Cliff,     ,   ,      1,      1,  ---


The givers are in the rows, i.e. Sam has given a gift to Nik once and to Murdoch twice.

Cells can be left blank; this is interpreted as the value 0. For instance, William has not given a gift to Murdoch. The diagonal values are ignored.

Notably, this format is pretty friendly for working with Google Sheets (and possibly most similar programs). You can keep track of gifts there and import the required .csv file.

## Implementation notes

* To be exact, this script tries to minimize the maximum value of every row. As a result, the numbers of gifts a particular person has given to everybody else should be fairly balanced at all times.
* There will be often multiple arrangements of givers and recievers that are equally good by the above definition. One possibility is randomly picked.
* Everything else that would indicate a "good" Secret Santa round according to some interpretations is ignored. There may be smaller cycles, i.e. person A can give a gift to person B who gives back to person A. In some cases, a person may give a gift to the same person multiple times in a row.
* The whole thing works by bruteforce and most likely can't be used for more than 15 people or so. I imagine this will not be a huge issue as most use cases are likely to be small groups of friends. If you hit the performance limit, feel free to rewrite this in Rust or get rid of some of your friends I guess