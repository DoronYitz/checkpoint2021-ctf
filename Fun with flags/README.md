# Fun with flags

---

In this challenge we have message, and a interactive shell using netcat, and `flags.py` which is a server file

##### Message

```
Welcome to Dr. Sheldon Cooper and Dr. Amy Farrah Fowler's flags shop!
Where you can buy and sell some of our favorite flags.
Colors? Stripes? Stars? We've got them all!
We've given you some coins, don't spend them all at once :)
Hope you'll have Fun With Flags!
Disclaimer:
Dr. Sheldon Cooper, who created the shop, allowed only himself to buy certain flags, so don't
be disappointed if you can't have all of them.
He also decided to log every transaction, in case anyone tries to buy the special flags that are
not allowed, so don't try to trick him!
```

```
nc fun-with-flags.csa-challenge.com 6666
```

##### Goal

We need to buy the flag of CSA, which we assume be the flag.

##### Solution

After reading carefully the source code we notice 2 things we could exploit:

First one:

```
 try:
		if 0 <= flag_index < len(user.owned_flags):
				flag_to_sell = user.owned_flags[flag_index]
				log_message = str(user) + " is selling flag " + flag_to_sell.name
		else:
				log_message = str(user) + " is trying to sell a flag they don't have. This looks suspicious!"
				send("Invalid flag index. This attempt is logged!")

		if flag_to_sell is not None:
				user.sell_flag(flag_to_sell)
				available_flags.append(flag_to_sell)
				send(f"{flag_to_sell.name} flag sold!")
				log_message += f". {flag_to_sell.name} Sold successfully!"
```

Means we can sell a flag twice when using index that meets `0 <= flag_index`, and make unlimited amount of money

Second one:

```
try:
		if 0 <= flag_index < len(available_flags):
				flag_to_buy = available_flags[flag_index]
				allowed_to_buy_flag = user.can_afford_flag(flag_to_buy)
				log_message = str(user) + f" is trying to buy flag {flag_to_buy.name}"
				if flag_to_buy.name == "CSA":
						log_message += "\n***ATTENTION - CSA FLAG PURCHASE. RUNNING ADDITIONAL CHECK***"
						allowed_to_buy_flag = allowed_to_buy_flag and user.allowed_to_buy_CSA_flag()
						log_message += " Additional checks result - user is " + ("ALLOWED" if allowed_to_buy_flag else "NOT ALLOWED") + " to purchase it"

				send("You tried to buy flag " + flag_to_buy.name + " (allowed to purchase? " + str(allowed_to_buy_flag) + "). This transaction was logged successfully.")
		else:
				log_message = str(user) + " is trying to buy an non-existing flag. This looks suspicious!"
				send("Invalid flag index. This attempt is logged!")

		open("log.txt", "a+").write(log_message + "\n")
except:
		send(f'Failed to log transaction of flag purchase. Do you have write permission?')

if flag_to_buy is not None:
		if allowed_to_buy_flag:
				user.buy_flag(flag_to_buy)
				available_flags.remove(flag_to_buy)
				send(f"{flag_to_buy.name} flag bought!")
		else:
				send(f"You can't buy flag {flag_to_buy.name}!")
```

In the code above, if there is any exception, we move to except part, check if the flag_to_buy is not None, and buy it.
Now lets find out how we can create an exception!

###### Divide by zero exception

```
log_message = str(user) + f" is trying to buy flag {flag_to_buy.name}"
```

It uses str(user), which include line like:

```
result += "star (total {}) - {:0.2f}.\n".format(total_stars, user_value / total_stars)
```

All we need to do now, is to make sure we have zero total stars - and this method will throw the exception
We can ensure it with the following sequence:

- Sell all our flags
- Buy russia flag which have 0 stars.

##### Plan:

- Make enough money to buy CSA special flag and Russia flag
- Sell all ours flags
- Buy Russia flag (and have total 0 stars)
- Try to buy CSA flag
- Exception will be thrown
- Flag achieved

##### Flag

```
CSA{M4y_Th3Re_ALwaY5_8E_A_ST4R_0n_y0UR_fL4G}
```
