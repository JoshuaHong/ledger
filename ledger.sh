#!/bin/bash
#
# Adds a transaction to the ledger in the following format:
# Category|Subcategory|Items|Amount|Location|Timestamp|Method of Payment|
#   Description|Receipt
#
# Optional dependencies: fzf
# Usage: ./ledger.sh

set -o errexit
set -o nounset
set -o pipefail

declare -a dependencies=("fzf")

declare transaction=""

main() {
    menu
}

# The main menu.
# Provides the option to add, edit, or delete a transaction.
menu() {
    echo "Manage transactions:"
    local -a options=("Add add" "Edit edit" "Delete delete")
    selectOption "${options[@]}"
}

# Adds a transaction to the ledger.
add() {
    echo "ADD"
}

# Edits a transaction to the ledger.
edit() {
    echo "EDIT"
}

# Deletes a transaction to the ledger.
delete() {
    echo "DELETE"
}

# Helper method to select an option.
# Parameters:
#     options: An array of pairs. The first parameter in the pair denotes the
#              name of the option, the second parameter in the pair denotes the
#              name of the function to call if it is selected.
selectOption() {
    local -a options=("${@}")
    local -i numOptions="${#options[@]}"
    select option in "${options[@]%% *}"; do
        if isInteger "${REPLY}" \
                && (( "${REPLY}" >= 1 && "${REPLY}" <= "${numOptions}" )); then
            "${options["${REPLY}" - 1]##* }"  # Execute the selected function.
            return
        else
            echoError "Error: Unsupported option."
        fi
    done
}

assertDependencies() {
    local -n dependencies="${1}"
    for depencency in "${dependencies[@]}"; do
        if ! command -v "${depencency}" &> /dev/null; then
            echoError "Error: Missing depencency \"${depencency}\"."
            exit 1
        fi
    done
}

isInteger() {
    local variable="${1}"
    local integerRegex="^-?[0-9]+$"
    [[ "${variable}" =~ ${integerRegex} ]]
}

echoError() {
    echo "${@}" 1>&2
}

main
