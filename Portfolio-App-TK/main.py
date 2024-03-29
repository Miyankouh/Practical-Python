from tkinter import *
from tkinter import messagebox, Menu
import requests
import json
import sqlite3


py_crypto = Tk()
py_crypto.title("My Crypto Portfolio") # Adding a title
py_crypto.iconbitmap("favicon.ico") # in windows

# Function to display letters in large format
def caps(event):
    v.set(v.get().upper())

v = StringVar()


con = sqlite3.connect("coin.db")
cursor_obj = con.cursor()
cursor_obj.execute(
    "CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY, symbol TEXT, amount INTEGER, price REAL)"
)
con.commit()


def reset():
    for cell in py_crypto.winfo_children():
        cell.destroy()

    app_nav()
    app_header()
    my_portfolio()


def app_nav():
    def clear_all():
        cursor_obj.execute("DELETE FROM coin")
        con.commit()

        messagebox.showinfo(
            "Portfolio Notification", "Portfolio Cleared - Add New Coins"
        )
        reset()

    def close_app():
        py_crypto.destroy()

    menu = Menu(py_crypto)
    file_item = Menu(menu)
    file_item.add_command(label="Clear Portfolio", command=clear_all)
    file_item.add_command(label="Close App", command=close_app)
    menu.add_cascade(label="File", menu=file_item)
    py_crypto.config(menu=menu)


def my_portfolio():
    api_request = requests.get(
        "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=ae5ce47b-8a4f-4b21-80ea-a5b7504cd77d"
    )
    api = json.loads(api_request.content)

    cursor_obj.execute("SELECT * FROM coin")
    coins = cursor_obj.fetchall()

    # color function
    def font_color(amount):
        if amount >= 0:
            return "green"
        else:
            return "red"

    def insert_coin():
        cursor_obj.execute(
            "INSERT INTO coin(symbol, price, amount) VALUES(?, ?, ?)",
            (symbol_txt.get(), price_txt.get(), amount_txt.get()),
        )
        con.commit()

        messagebox.showinfo(
            "Portfolio Notification", "Coin Added To Portfolio Successfully!"
        )
        reset()

    def update_coin():
        cursor_obj.execute(
            "UPDATE coin SET symbol=?, price=?, amount=? WHERE id=?",
            (
                symbol_update.get(),
                price_update.get(),
                amount_update.get(),
                portid_update.get(),
            ),
        )
        con.commit()

        messagebox.showinfo("Portfolio Notification", "Coin Updated Successfully!")
        reset()

    def delete_coin():
        cursor_obj.execute("DELETE FROM coin WHERE id=?", (portid_delete.get(),))
        con.commit()

        messagebox.showinfo("Portfolio Notification", "Coin Deleted From Portfolio")
        reset()

    total_pl = 0
    coin_row = 1
    total_current_value = 0
    total_amount_paid = 0

    for i in range(0, 300):
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:
                total_paid = coin[2] * coin[3]
                current_value = coin[2] * api["data"][i]["quote"]["USD"]["price"]
                pl_percoin = api["data"][i]["quote"]["USD"]["price"] - coin[3]
                total_pl_coin = pl_percoin * coin[2]

                total_pl += total_pl_coin
                total_current_value += current_value
                total_amount_paid += total_paid

                portfolio_id = Label(
                    py_crypto,
                    text=coin[0],
                    bg="#F3F4F6",
                    fg="black",
                    font="Lato 12",
                    borderwidth=2,
                    relief="groove",
                    padx="2",
                    pady="2",
                )
                portfolio_id.grid(row=coin_row, column=0, sticky=N + S + E + W)

                name = Label(
                    py_crypto,
                    text=api["data"][i]["symbol"],
                    bg="#F3F4F6",
                    fg="black",
                    font="Lato 12",
                    borderwidth=2,
                    relief="groove",
                    padx="2",
                    pady="2",
                )
                name.grid(row=coin_row, column=1, sticky=N + S + E + W)

                price = Label(
                    py_crypto,
                    text="${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]),
                    bg="#F3F4F6",
                    fg="black",
                    font="Lato 12",
                    borderwidth=2,
                    relief="groove",
                    padx="2",
                    pady="2",
                )
                price.grid(row=coin_row, column=2, sticky=N + S + E + W)

                no_coins = Label(
                    py_crypto,
                    text=coin[2],
                    bg="#F3F4F6",
                    fg="black",
                    font="Lato 12",
                    borderwidth=2,
                    relief="groove",
                    padx="2",
                    pady="2",
                )
                no_coins.grid(row=coin_row, column=3, sticky=N + S + E + W)

                amount_paid = Label(
                    py_crypto,
                    text="${0:.2f}".format(total_paid),
                    bg="#F3F4F6",
                    fg="black",
                    font="Lato 12",
                    borderwidth=2,
                    relief="groove",
                    padx="2",
                    pady="2",
                )
                amount_paid.grid(row=coin_row, column=4, sticky=N + S + E + W)

                current_val = Label(
                    py_crypto,
                    text="${0:.2f}".format(current_value),
                    bg="#F3F4F6",
                    fg="black",
                    font="Lato 12",
                    borderwidth=2,
                    relief="groove",
                    padx="2",
                    pady="2",
                )
                current_val.grid(row=coin_row, column=5, sticky=N + S + E + W)

                pl_coin = Label(
                    py_crypto,
                    text="${0:.2f}".format(pl_percoin),
                    bg="#F3F4F6",
                    fg=font_color(float("{0:.2f}".format(pl_percoin))),
                    font="Lato 12",
                    borderwidth=2,
                    relief="groove",
                    padx="2",
                    pady="2",
                )
                pl_coin.grid(row=coin_row, column=6, sticky=N + S + E + W)

                totalpl = Label(
                    py_crypto,
                    text="${0:.2f}".format(total_pl_coin),
                    bg="#F3F4F6",
                    fg=font_color(float("{0:.2f}".format(total_pl_coin))),
                    font="Lato 12",
                    borderwidth=2,
                    relief="groove",
                    padx="2",
                    pady="2",
                )
                totalpl.grid(row=coin_row, column=7, sticky=N + S + E + W)

                coin_row += 1

    # INSERT COIN
    symbol_txt = Entry(py_crypto, textvariable=v, borderwidth=2, relief="groove")
    py_crypto.bind("<KeyRelease>", caps) # 
    symbol_txt.grid(row=coin_row + 1, column=1)

    price_txt = Entry(py_crypto, borderwidth=2, relief="groove")
    price_txt.grid(row=coin_row + 1, column=2)

    amount_txt = Entry(py_crypto, borderwidth=2, relief="groove")
    amount_txt.grid(row=coin_row + 1, column=3)

    add_coin = Button(
        py_crypto,
        text="Add Coin",
        bg="#142E54",
        fg="white",
        command=insert_coin,
        font="Lato 12",
        borderwidth=2,
        relief="groove",
        padx="2",
        pady="2",
    )
    add_coin.grid(row=coin_row + 1, column=4, sticky=N + S + E + W)

    # UPDATE COIN
    portid_update = Entry(py_crypto, borderwidth=2, relief="groove")
    portid_update.grid(row=coin_row + 2, column=0)

    symbol_update = Entry(py_crypto, borderwidth=2, relief="groove")
    symbol_update.grid(row=coin_row + 2, column=1)

    price_update = Entry(py_crypto, borderwidth=2, relief="groove")
    price_update.grid(row=coin_row + 2, column=2)

    amount_update = Entry(py_crypto, borderwidth=2, relief="groove")
    amount_update.grid(row=coin_row + 2, column=3)

    update_coin_txt = Button(
        py_crypto,
        text="Update Coin",
        bg="#142E54",
        fg="white",
        command=update_coin,
        font="Lato 12",
        borderwidth=2,
        relief="groove",
        padx="2",
        pady="2",
    )
    update_coin_txt.grid(row=coin_row + 2, column=4, sticky=N + S + E + W)

    # DELETE COIN
    portid_delete = Entry(py_crypto, borderwidth=2, relief="groove")
    portid_delete.grid(row=coin_row + 3, column=0)

    delete_coin_txt = Button(
        py_crypto,
        text="Delete Coin",
        bg="#142E54",
        fg="white",
        command=delete_coin,
        font="Lato 12",
        borderwidth=2,
        relief="groove",
        padx="2",
        pady="2",
    )
    delete_coin_txt.grid(row=coin_row + 3, column=4, sticky=N + S + E + W)

    totalap = Label(
        py_crypto,
        text="${0:.2f}".format(total_amount_paid),
        bg="#F3F4F6",
        fg="black",
        font="Lato 12",
        borderwidth=2,
        relief="groove",
        padx="2",
        pady="2",
    )
    totalap.grid(row=coin_row, column=4, sticky=N + S + E + W)

    totalcv = Label(
        py_crypto,
        text="${0:.2f}".format(total_current_value),
        bg="#F3F4F6",
        fg="black",
        font="Lato 12",
        borderwidth=2,
        relief="groove",
        padx="2",
        pady="2",
    )
    totalcv.grid(row=coin_row, column=5, sticky=N + S + E + W)

    totalpl = Label(
        py_crypto,
        text="${0:.2f}".format(total_pl),
        bg="#F3F4F6",
        fg=font_color(float("{0:.2f}".format(total_pl))),
        font="Lato 12",
        borderwidth=2,
        relief="groove",
        padx="2",
        pady="2",
    )
    totalpl.grid(row=coin_row, column=7, sticky=N + S + E + W)

    api = ""

    refresh = Button(
        py_crypto,
        text="Refresh",
        bg="#142E54",
        fg="white",
        command=reset,
        font="Lato 12",
        borderwidth=2,
        relief="groove",
        padx="2",
        pady="2",
    )
    refresh.grid(row=coin_row + 1, column=7, sticky=N + S + E + W)


def app_header():
    portfolio_id = Label(
        py_crypto,
        text="Portfolio ID",
        bg="#142E54",
        fg="white",
        font="Lato 12 bold",
        padx="5",
        pady="5",
        borderwidth=2,
        relief="groove",
    )
    portfolio_id.grid(row=0, column=0, sticky=N + S + E + W)

    name = Label(
        py_crypto,
        text="Coin Name",
        bg="#142E54",
        fg="white",
        font="Lato 12 bold",
        padx="5",
        pady="5",
        borderwidth=2,
        relief="groove",
    )
    name.grid(row=0, column=1, sticky=N + S + E + W)

    price = Label(
        py_crypto,
        text="Price",
        bg="#142E54",
        fg="white",
        font="Lato 12 bold",
        padx="5",
        pady="5",
        borderwidth=2,
        relief="groove",
    )
    price.grid(row=0, column=2, sticky=N + S + E + W)

    no_coins = Label(
        py_crypto,
        text="Coin Owned",
        bg="#142E54",
        fg="white",
        font="Lato 12 bold",
        padx="5",
        pady="5",
        borderwidth=2,
        relief="groove",
    )
    no_coins.grid(row=0, column=3, sticky=N + S + E + W)

    amount_paid = Label(
        py_crypto,
        text="Total Amount Paid",
        bg="#142E54",
        fg="white",
        font="Lato 12 bold",
        padx="5",
        pady="5",
        borderwidth=2,
        relief="groove",
    )
    amount_paid.grid(row=0, column=4, sticky=N + S + E + W)

    current_val = Label(
        py_crypto,
        text="Current Value",
        bg="#142E54",
        fg="white",
        font="Lato 12 bold",
        padx="5",
        pady="5",
        borderwidth=2,
        relief="groove",
    )
    current_val.grid(row=0, column=5, sticky=N + S + E + W)

    pl_coin = Label(
        py_crypto,
        text="P/L Per Coin",
        bg="#142E54",
        fg="white",
        font="Lato 12 bold",
        padx="5",
        pady="5",
        borderwidth=2,
        relief="groove",
    )
    pl_coin.grid(row=0, column=6, sticky=N + S + E + W)

    totalpl = Label(
        py_crypto,
        text="Total P/L With Coin",
        bg="#142E54",
        fg="white",
        font="Lato 12 bold",
        padx="5",
        pady="5",
        borderwidth=2,
        relief="groove",
    )
    totalpl.grid(row=0, column=7, sticky=N + S + E + W)

# call Func
app_nav()
app_header()
my_portfolio()
py_crypto.mainloop()


# close connect
cursor_obj.close()
con.close()
