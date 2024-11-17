IMAGES = abstract-light-painting.png alaska-railroad.png blue-hour-paris.png \
	lower-kananaskis-lake.png marlet2-radio-board.png nikos-cat.png \
	pizza-food-wallpaper.png the-enchanted-garden.png tokyo-skytree-aerial.png

build: shuffled_images build_message

reconstruct: $(foreach img,$(IMAGES),$(patsubst %,images/reconstructed/%,$(img))) reconstruct_message

clean:
	rm -rf images/reconstructed/* images/shuffled/* tsp/*/*

original_images: $(foreach img,$(IMAGES),$(patsubst %,images/original/%,$(img)))

shuffled_images: $(foreach img,$(IMAGES),$(patsubst %,images/shuffled/%,$(img)))

build_message:
	@echo
	@echo "Now run 'make reconstruct' to reconstruct the images"

reconstruct_message:
	@echo
	@echo "The reconstructed images are in images/reconstructed"

.PHONY: build reconstruct clean original_images shuffled_images build_message reconstruct_message
.SECONDARY: # Retain all intermediate files


tsp/instances/%.tsp: images/shuffled/%.png
	bin/compute_scores.py "$<" > "$@"

tsp/tours/%.tour: tsp/instances/%.tsp
	bin/lkh.sh "$<" "$@"

images/shuffled/%.png: images/original/%.png
	bin/shuffle_image.py "$<" > "$@"

images/reconstructed/%.png: tsp/tours/%.tour
	bin/reconstruct_image.py "$<" images/shuffled/"$*".png > "$@"
