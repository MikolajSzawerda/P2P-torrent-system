import subprocess

state = {"connected": False}

while True:
    if not state["connected"]:
        user_input = input("Not connected to the network. Please type 'connect' to establish a connection: ")
    else:
        user_input = input("Enter a command (or 'disconnect' to disconnect, 'exit' to quit): ")

    if user_input.lower() == 'exit':
        print("Exiting the loop.")
        break

    if user_input.lower() == 'connect':
        state["connected"] = True
    if user_input.lower() == 'disconnect':
        state["connected"] = False

    process = subprocess.run(["python3", "ui_typer.py", user_input], capture_output=True, text=True)
    print(process.stdout)

print("End of the interaction loop.")
