# Prodebate

## Setup
- Install Docker and docker-compose
- `git clone`
- `docker-compose up`

## To Do

### Smaller stuff
- when form errors, return with correct URL params

### Bigger stuff, sooner
- Manifestation models.
	- Spin out into into its own app?
	- Refactor to allow the same URL to be applied to multiple notes
	- Error handling / URL normalizing on submit
	- External URL or Prodebate position
- Edit things
- Error handling
- Get tags working
- Make sure it's easy to spin up a new instance and populate sample data
- Private/draft points?

### Bigger stuff, later
- I think URLs need to be drastically rethought. They weren't well-thought-out in the first place. I don't like how everything is pretty dependent on GET params. 
- Grandparents might need to go into the elaboration model because without that you can only ever respond to the parent point. See conceptual discussion.
- Unit tests! Models are really simple now (no methods to test) and views are in flux. If I stay with Django views for awhile I should write tests; if I go to DRF then the whole game changes.
- Refine comments. Kinda want to see how they're used first, though some Bootstrapping couldn't hurt 'em.

### Conceptual Discussions
- Grandparents: I say "school uniforms should be mandated" and the counterpoint is "the U.S. Constitution mandates freedom of expression", and I counter with "students are not guaranteed Constitutional rights", that last argument doesn't entirely make sense if the first argument isn't in the tree.
- The most obvious solution then might be to add grandparent to the model if we're in a ...