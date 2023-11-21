import os


def setup_env():
    env_file = "chat_moder/.env"
    example_file = "chat_moder/.env.example"

    with open(example_file, "r") as example:
        with open(env_file, "w") as env:
            env.write(example.read())

    update_env_variable(env_file, "VIRUS_TOTAL_APIKEY")
    update_env_variable(env_file, "TELEGRAM_BOT_TOKEN")
    update_env_variable(env_file, "TELEGRAM_CHAT_ID")

    print("Setup complete.")


def update_env_variable(env_file, variable_name):
    value = input(f"Enter {variable_name}: ")
    os.system(f"sed -i 's/{variable_name}=/&{value}/' {env_file}")


if __name__ == "__main__":
    setup_env()
