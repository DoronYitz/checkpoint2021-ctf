# Computed shopping assistant

---

In this challenge we have message, and a interactive shell using netcat, and 3 files.

- main.c
- shopping_cart.c
- shopping_cart.h

##### Message

> Welcome to Computed Shopping Assistant!
> The place where you can manage your shopping cart, and get substantial discounts with our special promotion coupons!
> We have given all CSA candidates a free 10% OFF coupon:
> NOT_A_FLAG{I_4M_A_N3WB1E}
> Enjoy!
> Please be aware that the system is not perfect, so don't go around buying loaves of soup...

```

nc csa.csa-challenge.com 1111

```

##### Goal

We need to apply the 50% coupon

##### Solution

After reading carefully the message we pay attention to the clue says:

> Please be aware that the system is not perfect, so don't go around buying loaves of soup...

By reviewing the code we found out:

```

bool can_edit_item(item\* item){
if ((item->type == TYPE_UNDEFINED)) {
printf("There is no item at selected index\n");
return false;
} else if
(((item->type == TYPE_BREAD) && (item->grocery_item.amount_loaves > 0)) || ((item->type == TYPE_PASTA) && (item->grocery_item.amount_kilograms > 0)) ||
((item->type == TYPE_SOUP) && (item->grocery_item.amount_liters > 0)) || ((item->type == TYPE_DRINK) && (item->grocery_item.amount_liters > 0)) ||
((item->type == TYPE_VEGETABLE) && (item->grocery_item.amount_kilograms > 0)) || ((item->type = TYPE_FRUIT) && (item->grocery_item.amount_items > 0))) {
return true;
} else if ((item->type = TYPE_COUPON)) {
printf("Item is a coupon!\n");
return false;
} else {
printf("Invalid item type!\n");
return false;
}
}

```

There is a bug, at `item->type = TYPE_COUPON` & `item->type = TYPE_FRUIT`, using assignment instead of comparsion.
**Means we can turn coupon into a fruit, and a fruit into a coupon.**
We can use this bug later on.

Lets check how to we use the weakness of memory allocation of union to override have_entered property.

One cause of the union - have_entered and amount_kilograms have the same allocated memory, which is the second bug

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

struct shopping_cart_item {
enum item_type type;
union {
struct coupon_item coupon;
struct grocery_item grocery_item;
};
};

```

Plan:

- Insert any string and load both coupons into our cart, both not applyed
- Edit item on index 1 (Which is the 50% coupon) set amount_of_kilograms to `1`
- Right now the coupon has_entered prop is 1, but the computed shopping assistant wont show it cause it thinks it is a fruit.
- We can turn fruit into a coupon using the bug we found above.
- Edit item on index 1, set amount of items to `0` - Which turns the fruit into a coupon
- View our shopping cart

##### Flag

```

CSA{iN_L1nuX_1T_W0UlDnT_H4PP3N}

```

```

```
