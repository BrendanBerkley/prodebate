# Prodebate

## Setup
- Install Docker and docker-compose
- `git clone`
- `docker-compose up`

## To Do

### Smaller stuff

- General elaboration to real django form
- All point/elaboration forms should probably have the same view logic
- grandparent into elaboration model (and into links)?
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
- Unit tests! Models are really simple now (no methods to test) and views are in flux. If I stay with Django views for awhile I should write tests; if I go to DRF then the whole game changes.
- Refine comments. Kinda want to see how they're used first, though some Bootstrapping couldn't hurt 'em.