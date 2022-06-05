#    Strange game

---

In this challenge we have message, and a interactive game using netcat

##### The message

> It's just winning a simple game. What could go wrong?

```
nc strange-game.csa-challenge.com 4444
```

##### Game rules

After using netcat we found out the game rules are:

![](../Strange%20Game/rules.png)

Our goal:

- Win or tie all 15 rounds to get the flag.

##### Solution

- Using magic square logic to turn the problem into a simple tic-tac-toe game.
- Later on we found out another clue by searching on google "A strange game"
- Check https://en.wikipedia.org/wiki/Magic_square for futher information

```
# Magic square
# Enhanced tic-tac-toe board with 1-9 numbers according to magic square rules
# All rows and columns sums are 15.
{  ,  ,  }        { 2 , 7 , 6 }
{  ,  ,  }   ->   { 9 , 5 , 1 }
{  ,  ,  }        { 4 , 3 , 8 }
```

##### Flag

The flag link has a reference to a scene in the movie, playing endless tic-tac-toe game against the pc

```
CSA{https://www.youtube.com/watch?v=NHWjlCaIrQo}
```
