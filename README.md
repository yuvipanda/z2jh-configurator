# z2jh-configurator

A GUI based configurator for some admin tasks performed on a z2jh based JupyterHub

## Why?

The KubeSpawner `profileList` lets *end users* of the hub pick and choose
what kind of environment they want to use. This usually involves:

1. Picking what *image* to launch into, for their preferred environment
2. What kind of *resources* they want - memory, CPU, GPUs, disk sizes.

*Infrastructure admins* manage the underlying kubernetes cluster these users
land on, but currently also have to manage the `profileList`. This management,
particularly keeping the constantly changing list of images up to date, can
become quite a bit of [toil](https://sre.google/sre-book/eliminating-toil/).
And because infrastructure admin capacity is almost always limited, it might
also delay when users can use new images or other functionality.

`z2jh_configurator` separates management of the `profileList` from the underlying
infrastructure, and hands control of that to *JupyterHub admins*. They can change
images, provide appropriate resource guidelines and write useful descriptions
for end users. Their choices are still constrained by what Infrastructure
Admins provide - for example, information about available `NodeGroup`s are 
provided by Infrastructure admins, and this makes sense as those are just
*representations* of the underlying infrastructure that JupyterHub runs on.
Simply adding a `NodeGroup` in the UI isn't going to help when the underlying
nodes simply will not come up!

## Configurable options

JupyterHub admins can freely edit the following:

1. List of profiles, names and descriptions
2. List of images associated with each profile
3. NodeGroups that each profile should spawn into

Infrastructure admins provide *at deployment time* information about
the *list* of NodeGroups available, reflecting what has been provisioned.
