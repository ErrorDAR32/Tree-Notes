# Tree-Notes

This small program is designed to manage, store and work with a tree structure of notes.
each note represents a node in the tree, and each node able to have have multiple child nodes, and so fort.

To use it you just need to execute main.py file!

### Current Commands
_note: more commands will be added in the future_
- browse <node number>
    - To navigate to a subnode

- goup
    - The contrary to browse

- create
    - Creates a new subnode and prompts the "editor" (currently input()).

- delete <number> 
    - Deletes a subnode.

- edit <number>
    - Edits a subnode, if no argument is given edits the current browsed node.

- see <number>
    - Displays the text of a subnode, if no argument is given displays the current node text.
    
- preview
    - Displays a preview of the current node and all of his direct childs with each node number.

- rpreview
    - The same as preview, but it does it in a recursive manner.

- load file
    - Loads the contents of a file into memory, asuming it is a valid Tree-notes file.

- save file
    - Saves all the current loaded notes into human readable file.
    
- csave file
    - Saves the contents of memory into a non human friendly but more small file.
    
- exit
    - Exits the program without saving.
