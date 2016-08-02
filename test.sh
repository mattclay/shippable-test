#!/usr/bin/env python

print("\033[0;32mThis text should be green.")
print("This text should be green, but is probably white on Shippable.")
print("\033[0mThis text should be white.")

print("\0337You should not see this.\0338You should see this white text.")

print("\033[0;31mThis text should be red. \0337\033[0mThis text should be white. \0338\033[27CThis should be red.")
print("\033[0mThis text should be white.")

print("\033[0;34mThis text should be blue.")
print("\0337\033[0mThis text should be white. \0338\033[27CThis should be blue.")
print("\033[0mThis text should be white.")

print("\033[0;33mThis text should be yellow.\0337")
print("\033[0mThis text should be white. \0338\033[1B\033[1000D\033[27CThis should be yellow.")
print("\033[0mThis text should be white.")
