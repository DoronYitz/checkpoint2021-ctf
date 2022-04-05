# Computed shopping assistant II

---

This challenge opened after we've solved Computed shopping assistant I.
Minor modifications were maded to the source code.

- main.c
- shopping_cart.c
- shopping_cart.h

##### Message

```
Welcome to Computed Shopping Assistant II

Sadly, some users found a way to abuse the system and use a secret coupon.
This time, we have added a new coupon that can't be revealed!
Note: the flag is in the format of CSA{...}
```

```
nc csa-2.csa-challenge.com 2222
```

##### Goal

We need to apply the 100% coupon, to get the flag.

##### Differences in source code

```
In shopping_cart.h -
#define HIGH_DISCOUNT_AMOUNT 90

In main.c -
case TYPE_COUPON:
	if (item->coupon.have_entered) {
		if (item->coupon.discount_amount < HIGH_DISCOUNT_AMOUNT) {
			printf("(index %d) - %d%% OFF coupon - %s\n", i, item->coupon.discount_amount, item->coupon.code);
		} else { // need to be a little more discrete about special coupons
			printf("(index %d) - %d%% OFF coupon - *CENSORED*\n", i, item->coupon.discount_amount);
		}
	}
	break;

```

##### Solution

At first, we tryed the type confusion we've found in the first challenge and we noticed that: discount_amount and amount_grams allocated the same memory, but we cannot change amount_grams...

```
struct coupon_item {
	int discount_amount;
	int have_entered;
	int is_valid;
	int length;
	int expiration_day;
	int expiration_month;
	int expiration_year;
	char code[STRING_BUFFER_SIZE];
};

struct grocery_item {
	int amount_grams; // deprecated - use kilograms instead
	int amount_kilograms;
	int amount_items;
	int amount_loaves;
	int amount_liters;
	char description[STRING_BUFFER_SIZE];
};
```

By reviewing the code we found out:

- In the code section we can use a brute-force on memcmp function, because we can override coupon.length in the same method using type confussion.

```
void apply_a_coupon() {
	if (!loaded_coupons) {
		load_coupon("coupon_10.txt", 10);
		load_coupon("coupon_50.txt", 50);
		load_coupon("coupon_100.txt", 100);
		loaded_coupons = true;
	}
	printf("Please enter your coupon:\n");
	char newline;
	scanf("%c", &newline); // clear newline from buffer
	fgets(user_input, STRING_BUFFER_SIZE, stdin);

	for (int i = 0; i < SHOPPING_CART_SIZE; i++) {
		item* item = &shopping_cart.items[i];
		if (item->type == TYPE_COUPON && !item->coupon.have_entered) {
			if (!memcmp(item->coupon.code, user_input, item->coupon.length)) {
				printf("Applied coupon for %d%% OFF!\n", item->coupon.discount_amount);
				item->coupon.have_entered = true;
				return;
			}
		}
	}
	printf("Invalid coupon!\n");
}
```

Plan:

- Start with `CSA{` as the flag as the message says:
  `Note: the flag is in the format of CSA{...}`
- Iterate every `string.printable` character
- Change the length to current char length using `amount_loaves`
- After we found new character, reset the program to find the next character

##### Flag

```
CSA{Typ3_C0nFu510n_iS_a_ReAL_Pr0bL3m}
```
