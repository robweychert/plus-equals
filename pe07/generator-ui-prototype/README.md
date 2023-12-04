# Plus Equals #7 Generator UI Prototype

Read [*Plus Equals #7*](https://plusequals.art/07/) for the full backstory on this:

> I built an app that generates random mutations one at a time—either asymmetrical or radially symmetrical—and lets me sort them into “yes” and “no” piles. For each sorting session with the app, I tried not to think about it too much, letting instinct decide which variations were selected and which were rejected, continuing until I had 60 variations in the “yes” pile.

This UI began as a prototype for the random mutation generator featured in *Plus Equals #7*, and then I wound up using it to actually curate the content. The Tinder-style left and right cursor keys add an array of the current mutation’s deviation coordinates to the Yes (right) and No (left) `textarea`s before generating a new mutation. An alert appears when the Yes `textarea` has 60 mutations. Those coordinates can then be copied and used with `pe07.py` and [DrawBot](https://drawbot.com/) to output the mutations to PDF and SVG.