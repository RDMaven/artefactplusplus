#!/bin/sh
RED="\e[31m"
GREEN="\e[32m"
BLUE="\e[34m"
YELLOW="\e[33m"
END="\e[0m"
BOLD="\e[1m"

BLUE="\033[34m"
GREEN="\033[32m"
RED="\033[31m"
END="\033[0m"

line_start() {
  TEXT="$1"
  printf "%b" "${BLUE}${TEXT}${END}"
}

end_line() {
  local status="$1"
  local cols=$(tput cols)

  # compute dots using raw text length
  local dots=$((cols - ${#TEXT} - ${#status}))
  ((dots < 1)) && dots=1

  printf '%*s' "$dots" '' | tr ' ' '.'

  case "$status" in
    Done|OK|Found|Installed|"Already exists")
      printf "%b\n" "${GREEN}${status}${END}"
      ;;
    *)
      printf "%b\n" "${RED}${status}${END}"
      ;;
  esac
}


set -e

printf "%b" "${BLUE}Setting up project...${END}\n"

# Find python
line_start "> Looking for Python"
if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
elif command -v py >/dev/null 2>&1; then
    PYTHON=py
else
    end_line "Not Found"
    exit 1
fi
end_line "Found"


building_python () {
    CURPATH=$(pwd)
    printf "%b" "${YELLOW}${BOLD}> Building '$1' environment${END} \n"
    cd "$1"

    # Create virtual environment if it doesn't exist
    line_start "Creating virtual environment"
    if [ ! -d ".venv" ]; then
        "$PYTHON" -m venv .venv
        end_line "Done"
    else
        end_line "Already exists"
    fi

    # Activate venv
    line_start "Activating virtual environment"
    source .venv/bin/activate
    end_line "Done"

    # Upgrade pip
    line_start "Upgrading pip"
    pip install --upgrade pip >/dev/null
    end_line "Done"

    # Install requirements
    if [ -f "requirements.txt" ]; then
        line_start "Installing dependencies"
        pip install -r requirements.txt >/dev/null
        end_line "Done"
    else
    end_line "Warning: requirements.txt not found"
    fi

    cd "$CURPATH"
}

building_python "./client"
building_python "./server"

printf "%b" "${GREEN}${BOLD}Setup complete.${END}\n\n"

printf "%b" "${YELLOW}${BOLD}To launch the project, follow these instructions :${END}\n"
printf "%b" "${YELLOW}1) Please fill the 'client/.env' file. ${RED}(NOT 'client/.env.example' OR 'server/.env')${END}\n"
printf "%b" "${YELLOW}2) To start the client, run:${END}\n"
printf "%b" "  ${GREEN}./client/start.sh${END}\n"
printf "%b" "${YELLOW}3) To start the server, run:${END}\n"
printf "%b" "  ${GREEN}./server/start.sh${END}\n"