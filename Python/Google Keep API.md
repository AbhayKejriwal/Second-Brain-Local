### https://gkeepapi.readthedocs.io/en/latest/#welcome-to-gkeepapi-s-documentation

# [Welcome to gkeepapi’s documentation!](#id1)

Contents

- [](#)[Welcome to gkeepapi’s documentation!](#welcome-to-gkeepapi-s-documentation)
    
- [](#)[Client Usage](#client-usage)
    
    - [](#)[Logging in](#logging-in)
        
    - [](#)[Syncing](#syncing)
        
    - [](#)[Caching notes](#caching-notes)
        
- [](#)[Notes and Lists](#notes-and-lists)
    
    - [](#)[Creating Notes](#creating-notes)
        
    - [](#)[Getting Notes](#getting-notes)
        
    - [](#)[Searching for Notes](#searching-for-notes)
        
    - [](#)[Manipulating Notes](#manipulating-notes)
        
        - [](#)[Getting Note content](#getting-note-content)
            
        - [](#)[Getting List content](#getting-list-content)
            
        - [](#)[Setting Note content](#setting-note-content)
            
        - [](#)[Setting List content](#setting-list-content)
            
        - [](#)[Setting List item position](#setting-list-item-position)
            
        - [](#)[Sorting a List](#sorting-a-list)
            
        - [](#)[Indent/dedent List items](#indent-dedent-list-items)
            
    - [](#)[Deleting Notes](#deleting-notes)
        
- [](#)[Media](#media)
    
    - [](#)[Accessing media](#accessing-media)
        
    - [](#)[Fetching media](#fetching-media)
        
- [](#)[Labels](#labels)
    
    - [](#)[Getting Labels](#getting-labels)
        
    - [](#)[Searching for Labels](#searching-for-labels)
        
    - [](#)[Creating Labels](#creating-labels)
        
    - [](#)[Editing Labels](#editing-labels)
        
    - [](#)[Deleting Labels](#deleting-labels)
        
    - [](#)[Manipulating Labels on Notes](#manipulating-labels-on-notes)
        
- [](#)[Constants](#constants)
    
- [](#)[Annotations](#annotations)
    
- [](#)[Settings](#settings)
    
- [](#)[Collaborators](#collaborators)
    
- [](#)[Timestamps](#timestamps)
    
- [](#)[FAQ](#faq)
    
- [](#)[Known Issues](#known-issues)
    
- [](#)[Debug](#debug)
    
- [](#)[Notes](#notes)
    
    - [](#)[Reporting errors](#reporting-errors)
- [](#)[Indices and tables](#indices-and-tables)
    

**gkeepapi** is an unofficial client for programmatically interacting with Google Keep:

```
import gkeepapi

keep = gkeepapi.Keep()
keep.login('user@gmail.com', 'password')

note = keep.createNote('Todo', 'Eat breakfast')
note.pinned = True
note.color = gkeepapi.node.ColorValue.Red

keep.sync()

print(note.title)
print(note.text)
```

The client is mostly complete and ready for use, but there are some hairy spots. In particular, the interface for manipulating labels and blobs is subject to change.

# [Client Usage](#id2)

All interaction with Google Keep is done through a [`Keep`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep "gkeepapi.Keep") object, which is responsible for authenticating, syncing changes and tracking modifications.

## [Logging in](#id3)

gkeepapi leverages the mobile Google Keep API. To do so, it makes use of `gpsoauth`, which requires passing in the username and password. This was necessary as the API we’re using is restricted to Google applications (put differently, there is no way to enable it on the Developer Console):

```
keep = gkeepapi.Keep()
keep.login('...', '...')
```

To reduce the number of logins you make to the server, you can store the master token after logging in. Protect this like a password, as it grants full access to your account:

```
import keyring
# <snip>
token = keep.getMasterToken()
keyring.set_password('google-keep-token', username, token)
```

You can load this token at a later point:

```
import keyring
# <snip>
token = keyring.get_password('google-keep-token', username)
keep.resume(email, master_token)
```

Note: Enabling TwoFactor and logging in via an app password is recommended.

## [Syncing](#id4)

gkeepapi automatically pulls down all notes after login. It takes care of refreshing API tokens, so there’s no need to call [`Keep.login()`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep.login "gkeepapi.Keep.login") again. After making any local modifications to notes, make sure to call [`Keep.sync()`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep.sync "gkeepapi.Keep.sync") to update them on the server!:

```
keep.sync()
```

## [Caching notes](#id5)

The initial sync can take a while, especially if you have a lot of notes. To mitigate this, you can serialize note data to a file. The next time your program runs, it can resume from this state. This is handled via [`Keep.dump()`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep.dump "gkeepapi.Keep.dump") and [`Keep.restore()`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep.restore "gkeepapi.Keep.restore"):

```
# Store cache
state = keep.dump()
fh = open('state', 'w')
json.dump(state, fh)

# Load cache
fh = open('state', 'r')
state = json.load(fh)
keep.restore(state)
```

You can also pass the state directly to the [`Keep.login()`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep.login "gkeepapi.Keep.login") and [`Keep.resume()`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep.resume "gkeepapi.Keep.resume") methods:

```
keep.login(username, password, state=state)
keep.resume(username, master_token, state=state)
```

# [Notes and Lists](#id6)

Notes and Lists are the primary types of notes visible to a Google Keep user. gkeepapi exposes these two notes via the [`node.Note`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.Note "gkeepapi.node.Note") and [`node.List`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.List "gkeepapi.node.List") classes. For Lists, there’s also the [`node.ListItem`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.ListItem "gkeepapi.node.ListItem") class.

## [Creating Notes](#id7)

New notes are created with the [`Keep.createNote()`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep.createNote "gkeepapi.Keep.createNote") and [`Keep.createList()`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep.createList "gkeepapi.Keep.createList") methods. The [`Keep`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep "gkeepapi.Keep") object keeps track of these objects and, upon [`Keep.sync()`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep.sync "gkeepapi.Keep.sync"), will sync them if modifications have been made:

```
gnote = keep.createNote('Title', 'Text')

glist = keep.createList('Title', [
    ('Item 1', False), # Not checked
    ('Item 2', True)  # Checked
])

# Sync up changes
keep.sync()
```

## [Getting Notes](#id8)

Notes can be retrieved via [`Keep.get()`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep.get "gkeepapi.Keep.get") by their ID (visible in the URL when selecting a Note in the webapp):

```
gnote = keep.get('...')
```

To fetch all notes, use [`Keep.all()`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep.all "gkeepapi.Keep.all"):

```
gnotes = keep.all()
```

## [Searching for Notes](#id9)

Notes can be searched for via [`Keep.find()`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep.find "gkeepapi.Keep.find"):

```
# Find by string
gnotes = keep.find(query='Title')

# Find by filter function
gnotes = keep.find(func=lambda x: x.deleted and x.title == 'Title')

# Find by labels
gnotes = keep.find(labels=[keep.findLabel('todo')])

# Find by colors
gnotes = keep.find(colors=[gkeepapi.node.ColorValue.White])

# Find by pinned/archived/trashed state
gnotes = keep.find(pinned=True, archived=False, trashed=False)
```

## [Manipulating Notes](#id10)

Note objects have many attributes that can be directly get and set. Here is a non-comprehensive list of the more interesting ones.

Notes and Lists:

- `node.TopLevelNode.id` (Read only)
    
- `node.TopLevelNode.parent` (Read only)
    
- [`node.TopLevelNode.title`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.TopLevelNode.title "gkeepapi.node.TopLevelNode.title")
    
- `node.TopLevelNode.text`
    
- [`node.TopLevelNode.color`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.TopLevelNode.color "gkeepapi.node.TopLevelNode.color")
    
- [`node.TopLevelNode.archived`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.TopLevelNode.archived "gkeepapi.node.TopLevelNode.archived")
    
- [`node.TopLevelNode.pinned`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.TopLevelNode.pinned "gkeepapi.node.TopLevelNode.pinned")
    
- [`node.TopLevelNode.labels`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.TopLevelNode.labels "gkeepapi.node.TopLevelNode.labels")
    
- `node.TopLevelNode.annotations`
    
- `node.TopLevelNode.timestamps` (Read only)
    
- [`node.TopLevelNode.collaborators`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.TopLevelNode.collaborators "gkeepapi.node.TopLevelNode.collaborators")
    
- [`node.TopLevelNode.blobs`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.TopLevelNode.blobs "gkeepapi.node.TopLevelNode.blobs") (Read only)
    
- [`node.TopLevelNode.drawings`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.TopLevelNode.drawings "gkeepapi.node.TopLevelNode.drawings") (Read only)
    
- [`node.TopLevelNode.images`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.TopLevelNode.images "gkeepapi.node.TopLevelNode.images") (Read only)
    
- [`node.TopLevelNode.audio`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.TopLevelNode.audio "gkeepapi.node.TopLevelNode.audio") (Read only)
    

ListItems:

- `node.TopLevelNode.id` (Read only)
    
- `node.TopLevelNode.parent` (Read only)
    
- `node.TopLevelNode.parent_item` (Read only)
    
- `node.TopLevelNode.indented` (Read only)
    
- `node.TopLevelNode.text`
    
- `node.TopLevelNode.checked`
    

### [Getting Note content](#id11)

Example usage:

```
print gnote.title
print gnote.text
```

### [Getting List content](#id12)

Retrieving the content of a list is slightly more nuanced as they contain multiple entries. To get a serialized version of the contents, simply access [`node.List.text`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.List.text "gkeepapi.node.List.text") as usual. To get the individual [`node.ListItem`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.ListItem "gkeepapi.node.ListItem") objects, access [`node.List.items`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.List.items "gkeepapi.node.List.items"):

```
# Serialized content
print glist.text

# ListItem objects
glistitems = glist.items

# Checked ListItems
cglistitems = glist.checked

# Unchecked ListItems
uglistitems = glist.unchecked
```

### [Setting Note content](#id13)

Example usage:

```
gnote.title = 'Title 2'
gnote.text = 'Text 2'
gnote.color = gkeepapi.node.ColorValue.White
gnote.archived = True
gnote.pinned = False
```

### [Setting List content](#id14)

New items can be added via [`node.List.add()`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.List.add "gkeepapi.node.List.add"):

```
# Create a checked item
glist.add('Item 2', True)

# Create an item at the top of the list
glist.add('Item 1', True, gkeepapi.node.NewListItemPlacementValue.Top)

# Create an item at the bottom of the list
glist.add('Item 3', True, gkeepapi.node.NewListItemPlacementValue.Bottom)
```

Existing items can be retrieved and modified directly:

```
glistitem = glist.items[0]
glistitem.text = 'Item 4'
glistitem.checked = True
```

Or deleted via `node.ListItem.delete()`:

```
glistitem.delete()
```

### [Setting List item position](#id15)

To reposition an item (larger is closer to the top):

```
# Set a specific sort id
glistitem1.sort = 42

# Swap the position of two items
val = glistitem2.sort
glistitem2.sort = glistitem3.sort
glistitem3.sort = val
```

### [Sorting a List](#id16)

Lists can be sorted via [`node.List.sort_items()`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.List.sort_items "gkeepapi.node.List.sort_items"):

```
# Sorts items alphabetically by default
glist.sort_items()
```

### [Indent/dedent List items](#id17)

To indent a list item:

```
gparentlistitem.indent(gchildlistitem)
```

To dedent:

```
gparentlistitem.dedent(gchildlistitem)
```

## [Deleting Notes](#id18)

The `node.TopLevelNode.delete()` method marks the note for deletion (or undo):

```
gnote.delete()
gnote.undelete()
```

To send the node to the trash instead (or undo):

```
gnote.trash()
gnote.untrash()
```

# [Media](#id19)

Media blobs are images, drawings and audio clips that are attached to notes.

## [Accessing media](#id20)

Drawings:

- [`node.NodeDrawing.extracted_text`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.NodeDrawing.extracted_text "gkeepapi.node.NodeDrawing.extracted_text") (Read only)

Images:

- [`node.NodeImage.width`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.NodeImage.width "gkeepapi.node.NodeImage.width") (Read only)
    
- [`node.NodeImage.height`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.NodeImage.height "gkeepapi.node.NodeImage.height") (Read only)
    
- [`node.NodeImage.byte_size`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.NodeImage.byte_size "gkeepapi.node.NodeImage.byte_size") (Read only)
    
- [`node.NodeImage.extracted_text`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.NodeImage.extracted_text "gkeepapi.node.NodeImage.extracted_text") (Read only)
    

Audio:

- [`node.NodeAudio.length`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.NodeAudio.length "gkeepapi.node.NodeAudio.length") (Read only)

## [Fetching media](#id21)

To download media, you can use the [`Keep.getMediaLink()`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep.getMediaLink "gkeepapi.Keep.getMediaLink") method to get a link:

```
blob = gnote.images[0]
keep.getMediaLink(blob)
```

# [Labels](#id22)

Labels are short identifiers that can be assigned to notes. Labels are exposed via the [`node.Label`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.Label "gkeepapi.node.Label") class. Management is a bit unwieldy right now and is done via the [`Keep`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep "gkeepapi.Keep") object. Like notes, labels are automatically tracked and changes are synced to the server.

## [Getting Labels](#id23)

Labels can be retrieved via [`Keep.getLabel()`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep.getLabel "gkeepapi.Keep.getLabel") by their ID:

```
label = keep.getLabel('...')
```

To fetch all labels, use [`Keep.labels()`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep.labels "gkeepapi.Keep.labels"):

```
labels = keep.labels()
```

## [Searching for Labels](#id24)

Most of the time, you’ll want to find a label by name. For that, use [`Keep.findLabel()`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep.findLabel "gkeepapi.Keep.findLabel"):

```
label = keep.findLabel('todo')
```

Regular expressions are also supported here:

```
label = keep.findLabel(re.compile('^todo$'))
```

## [Creating Labels](#id25)

New labels can be created with [`Keep.createLabel()`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep.createLabel "gkeepapi.Keep.createLabel"):

```
label = keep.createLabel('todo')
```

## [Editing Labels](#id26)

A label’s name can be updated directly:

```
label.name = 'later'
```

## [Deleting Labels](#id27)

A label can be deleted with [`Keep.deleteLabel()`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep.deleteLabel "gkeepapi.Keep.deleteLabel"). This method ensures the label is removed from all notes:

```
keep.deleteLabel(label)
```

## [Manipulating Labels on Notes](#id28)

When working with labels and notes, the key point to remember is that we’re always working with [`node.Label`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.Label "gkeepapi.node.Label") objects or IDs. Interaction is done through the [`node.NodeLabels`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.NodeLabels "gkeepapi.node.NodeLabels") class.

To add a label to a note:

```
gnote.labels.add(label)
```

To check if a label is on a note:

```
gnote.labels.get(label.id) != None
```

To remove a label from a note:

```
gnote.labels.remove(label)
```

# [Constants](#id29)

- [`node.ColorValue`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.ColorValue "gkeepapi.node.ColorValue") enumerates valid colors.
    
- [`node.CategoryValue`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.CategoryValue "gkeepapi.node.CategoryValue") enumerates valid note categories.
    
- [`node.CheckedListItemsPolicyValue`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.CheckedListItemsPolicyValue "gkeepapi.node.CheckedListItemsPolicyValue") enumerates valid policies for checked list items.
    
- [`node.GraveyardStateValue`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.GraveyardStateValue "gkeepapi.node.GraveyardStateValue") enumerates valid visibility settings for checked list items.
    
- [`node.NewListItemPlacementValue`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.NewListItemPlacementValue "gkeepapi.node.NewListItemPlacementValue") enumerates valid locations for new list items.
    
- [`node.NodeType`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.NodeType "gkeepapi.node.NodeType") enumerates valid node types.
    
- [`node.BlobType`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.BlobType "gkeepapi.node.BlobType") enumerates valid blob types.
    
- [`node.RoleValue`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.RoleValue "gkeepapi.node.RoleValue") enumerates valid collaborator permissions.
    
- [`node.ShareRequestValue`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.ShareRequestValue "gkeepapi.node.ShareRequestValue") enumerates vaild collaborator modification requests.
    
- [`node.SuggestValue`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.SuggestValue "gkeepapi.node.SuggestValue") enumerates valid suggestion types.
    

# [Annotations](#id30)

READ ONLY TODO

# [Settings](#id31)

TODO

# [Collaborators](#id32)

Collaborators are users you’ve shared notes with. Access can be granted or revoked per note. Interaction is done through the [`node.NodeCollaborators`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.NodeCollaborators "gkeepapi.node.NodeCollaborators") class.

To add a collaborator to a note:

```
gnote.collaborators.add(email)
```

To check if a collaborator has access to a note:

```
email in gnote.collaborators.all()
```

To remove a collaborator from a note:

```
gnote.collaborators.remove(email)
```

# [Timestamps](#id33)

All notes and lists have a [`node.NodeTimestamps`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.NodeTimestamps "gkeepapi.node.NodeTimestamps") object with timestamp data:

```
node.timestamps.created
node.timestamps.deleted
node.timestamps.trashed
node.timestamps.updated
node.timestamps.edited
```

These timestamps are all read-only.

# [FAQ](#id34)

1.  I get a “NeedsBrowser”, “CaptchaRequired” or “BadAuthentication” `exception.LoginException` when I try to log in.

This usually occurs when Google thinks the login request looks suspicious. Here are some steps you can take to resolve this:

1.  Make sure you have the newest version of gkeepapi installed.
    
2.  Instead of logging in every time, cache the authentication token and reuse it on subsequent runs. See [here](https://github.com/kiwiz/keep-cli/blob/master/src/keep_cli/__main__.py#L106-L128) for an example implementation.
    
3.  If you have 2-Step Verification turned on, generating an App Password for gkeepapi is highly recommended.
    
4.  Upgrading to a newer version of Python (3.7+) has worked for some people. See this [issue](https://gitlab.com/AuroraOSS/AuroraStore/issues/217#note_249390026) for more information.
    
5.  If all else fails, try testing gkeepapi on a separate IP address and/or user to see if you can isolate the problem.
    
6.  I get a “DeviceManagementRequiredOrSyncDisabled” `exception.LoginException` when I try to log in.
    

This is due to the enforcement of Android device policies on your G-Suite account. To resolve this, you can try disabling that setting [here](https://admin.google.com/AdminHome?hl=no#MobileSettings:section=advanced&flyout=security).

3.  My notes take a long time to sync

Follow the instructions in the caching notes section and see if that helps. If you only need to update notes, you can try creating a new Google account. Share the notes to the new account and manage through there.

# [Known Issues](#id35)

1.  [`node.ListItem`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.ListItem "gkeepapi.node.ListItem") consistency

The [`Keep`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep "gkeepapi.Keep") class isn’t aware of new [`node.ListItem`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.ListItem "gkeepapi.node.ListItem") objects till they’re synced up to the server. In other words, [`Keep.get()`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.Keep.get "gkeepapi.Keep.get") calls for their IDs will fail.

# [Debug](#id36)

To enable development debug logs:

```
gkeepapi.node.DEBUG = True
```

# [Notes](#id37)

- Many sub-elements are read only.
    
- [`node.Node`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.Node "gkeepapi.node.Node") specific [`node.NewListItemPlacementValue`](https://gkeepapi.readthedocs.io/en/latest/gkeepapi.html#gkeepapi.node.NewListItemPlacementValue "gkeepapi.node.NewListItemPlacementValue") settings are not used.
    

## [Reporting errors](#id38)

Google occasionally ramps up changes to the Keep data format. When this happens, you’ll likely get a `exception.ParseException`. Please report this on Github with the raw data, which you can grab like so:

```
try:
    # Code that raises the exception
except gkeepapi.exception.ParseException as e:
    print(e.raw)
```

If you’re not getting an `exception.ParseException`, just a log line, make sure you’ve enabled debug mode.

# [Indices and tables](#id39)

- [Index](https://gkeepapi.readthedocs.io/en/latest/genindex.html)
    
- [Module Index](https://gkeepapi.readthedocs.io/en/latest/py-modindex.html)
    
- [Search Page](https://gkeepapi.readthedocs.io/en/latest/search.html)
    

# [gkeepapi](#)

### Navigation

### Quick search

©2017, Kai. | Powered by [Sphinx 7.2.6](https://www.sphinx-doc.org/) & [Alabaster 0.7.16](https://alabaster.readthedocs.io) | [Page source](https://gkeepapi.readthedocs.io/en/latest/_sources/index.rst.txt)

v: latest