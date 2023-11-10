import matplotlib.pyplot as plt
import numpy as np
from node import Node
from member import Member
import os

nodes = []
members = []

def prompt(cmd) -> str:
  return input(f"\n{cmd}\n> ")
  

def clear_lines():
  for i in range(os.get_terminal_size().columns // 2):
    os.system('cls' if os.name == 'nt' else 'clear')

clear_lines()
print("\nWelcome to Isaac's Truss Force Calculator.")
exit = False
while(exit == False):
  cmd = prompt("What would you like to do?")
  cmd = cmd.strip()
  subCmds = cmd.split(" ")
  if subCmds[0] == "new":
    if subCmds[1] == "node":
      if (len(subCmds) >=4):
        x = int(subCmds[2])
        y = int(subCmds[3])
        xSupport = bool(subCmds[4]) if len(subCmds) >= 6 else False
        ySupport = bool(subCmds[5]) if len(subCmds) >= 6 else False
        nodes.append(Node(x, y, xSupport, ySupport))
      elif (len(subCmds) >= 3):
        print(f"\nInvalid argument \x1B[3m\"{subCmds[2]}\"\x1B[0m")
      else:
        x = prompt("What is the x coordinate?")
        y = prompt("What is the y coordinate?")
    elif subCmds[1] == "member":
      if (subCmds[2] and subCmds[3]):
        members.append(Member(int(subCmds[2]),int(subCmds[3])))
        
    else:
      print(f"\nPlease specify a new type, for help type \"help new\"")
  elif subCmds[0] == "print":
    if subCmds[1] == "nodes":
      print("\n\033[4mNodes:\033[0m\n")
      for i in range(len(nodes)):
        node = nodes[i]
        print(f"node_{i}: {{\n  x: {node.x} \n  y: {node.y} \n  xSupport: {node.xSupport} \n  ySupport: {node.ySupport}\n}}")
  
  if cmd == "exit":
    exit = True
  