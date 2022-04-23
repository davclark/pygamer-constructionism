# [PyGamer](https://learn.adafruit.com/adafruit-pygamer/overview) [Constructionism](http://www.papert.org/articles/SituatingConstructionism.html)

In Mindstorms, Papert suggests that one day a group of parents might organically develop a learning community in which
"mathetic" thinking is scaffolded by ever evolving systems for creative exploration and learning. As Arlo Guthrie says
(paraphrased):

> You know, if one person, just one person does it they may think he's really sick, and they won't take him. And if two
> people, two people do it, in harmony, they may think they're both *cough* and they won't take either of them. And if
> three people do it, three, can you imagine, three people walking in, developing an ecosystem for creative exploration
> and learning and walking out. They may think it's an organization. And can you, can you imagine fifty people a day, I
> said fifty people a day developing an ecosystem for creative exploration and learning and walking out. And friends,
> they may think it's a movement! And that's what it is, the PyGamer Constructionism Movement, and all you got to do to
> join is play along the next time it comes around, with feeling. So we'll wait for it to come around, here and play
> together when it does!

So, I hope you'll join me.

## The setup

Please file an issue if any of this is unclear.

- [Get a PyGamer](https://www.adafruit.com/product/4242). There is a kit that is often out of stock that includes
  everything you could need. At a minimum, you'll also need:
  - A [battery](https://www.adafruit.com/product/4237) (unless you want to stay plugged in all the time)
  - A [speaker](https://www.adafruit.com/product/4227) - my initial experiments include music!

Install a reasonably recent version of [CircuitPython](https://circuitpython.org/board/pygamer/), and then install the
matching [Adafruit library bundle](https://circuitpython.org/libraries) by copying it directly onto the PyGamer
filesystem.

You'll need a text editor and potentially a way to access the serial terminal to interact directly with the
CircuitPython runtime. The beginner-friendly approach is to use the [Mu](https://codewith.mu/en/download) text editor,
but my experience is that it doesn't work well on Linux. I'm using neovim, but any editor with reasonable Python support
will do (Adafruit provides some [guidance and gotchas for
editors](https://learn.adafruit.com/welcome-to-circuitpython/recommended-editors) - note that neovim changes the default
swapfile location, so you need only worry about the note for vim on not-neo-vim). I am additionally using the `tio`
terminal emulator to interact with the CircuitPython console, though the official "advanced" instructions default to
`screen`.

If you're used to REPL-driven development, you will likely enjoy the ability to access the Python prompt via the
terminal!

## Experiments

### musical_snake

Similar to the classic game you might find on a nokia phone, but instead of growing until you run into yourself, the
primary concern is that when the snake crosses an object, the object makes a sound. Basically this allows you to
implement a kind of step sequencer that's controlled with a joystick. This idea was refined with Martin.
