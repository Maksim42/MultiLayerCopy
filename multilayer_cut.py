#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *

def plugin_func(image, active_layer, shiftX, shiftY):
	pdb.gimp_context_push()
	pdb.gimp_image_undo_group_start(image)
	selection = pdb.gimp_selection_save(image)
	
	layerList = image.layers
	for layer in layerList:
		if pdb.gimp_item_get_linked(layer):
			CopySelection(image, layer, [shiftX, shiftY])
			pdb.gimp_image_select_item(image, 2, selection)
	
	pdb.gimp_image_remove_channel(image, selection)
	pdb.gimp_image_undo_group_end(image)
	pdb.gimp_context_pop()

def CopySelection(image, layer, offset):
	pdb.gimp_edit_cut(layer)
	float_layer = pdb.gimp_edit_paste(layer, FALSE)
	float_layer.translate(offset[0], offset[1])
	
	pdb.gimp_floating_sel_to_layer(float_layer)
	copy_layer = gimp.image_list()[0].layers[0]
	
	while pdb.gimp_image_get_layer_position(image, layer) > (pdb.gimp_image_get_layer_position(image, copy_layer) + 1):
		pdb.gimp_image_lower_item(image, copy_layer)
	pdb.gimp_image_merge_down(image, copy_layer, 1)

register(
					"python-fu-multilayer-cut",
					"Вырезает и вставляет одновременно на связаных слоях",
					"Вырезает выделенную область на связаных слоях и вставляет",
					"Максим Ломако",
					"Максим Ломако (maksim.lomako@gmail.com)",
					"05.07.2017",
					"Multilayer Cut",
					"*",
					[
							(PF_IMAGE, "image", "Исходное изображение", None),
							(PF_DRAWABLE, "active_layer", "Исходный слой", None),
							(PF_INT, "shiftX", "Сдвиг по X", "32"),
							(PF_INT, "shiftY", "Сдвиг по Y", "0"),
					],
					[],
					plugin_func, menu="<Image>/Multilayer/")

main()