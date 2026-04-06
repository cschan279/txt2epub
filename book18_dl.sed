s/book18.org$//g
s/^　　//g
s/ 　　/\n/g

# Replace "」   「" with "」\n「"
:space_loop
s/」[[:space:]]\+「/」\n「/
t space_loop

# Replace "。" with "。\n" unless immediately followed by "」"
:dot_loop
s/。\([^」\n]\)/。\n\1/
t dot_loop


# Ensure newline after "」" when not already followed by newline
:closing_loop
s/」\([^\n]\)/」\n\1/
t closing_loop


# Insert newline before "「" when not at line start
:open_loop
s/\([^\n]\)「/\1\n「/
t open_loop