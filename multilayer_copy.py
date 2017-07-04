#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *

def plugin_func(image, active_layer, shiftX, shiftY):
	pdb.gimp_context_push()
	pdb.gimp_image_undo_group_start(image)
	
	layerList = image.layers
	#layer = pdb.gimp_image_get_active_layer(image) #layer for
	for layer in layerList:
		if pdb.gimp_item_get_linked(layer):
			CopySelection(image, layer, [shiftX, shiftY])
	
	pdb.gimp_image_undo_group_end(image)
	pdb.gimp_context_pop()

def CopySelection(image, layer, offset):
	pdb.gimp_edit_copy(layer)
	float_layer = pdb.gimp_edit_paste(layer, FALSE)
	float_layer.translate(offset[0], offset[1])
	
	pdb.gimp_floating_sel_to_layer(float_layer)
	copy_layer = gimp.image_list()[0].layers[0]
	
	while pdb.gimp_image_get_layer_position(image, layer) > (pdb.gimp_image_get_layer_position(image, copy_layer) + 1):
		pdb.gimp_image_lower_item(image, copy_layer)
	pdb.gimp_image_merge_down(image, copy_layer, 1)

register(
					"python-fu-multilayer-copyShift",
					"Копирование и вставляет одновременно на нескольких слоях",
					"Копирует выделенную область на всех слоях и вставляет",
					"Максим Ломако",
					"Максим Ломако (maksim.lomako@gmail.com)",
					"04.07.2017",
					"Multilayer Copy-Shift", # Название пункта меню, с помощью которого дополнение будет запускаться
					"*", # Типы изображений, с которыми может работать дополнение
					[
							(PF_IMAGE, "image", "Исходное изображение", None), # Параметры, которые будут переданы дополнению
							(PF_DRAWABLE, "active_layer", "Исходный слой", None),# Всякие указатели на изображение, слои и т.д.
							(PF_INT, "shiftX", "Сдвиг по X", "32"),
							(PF_INT, "shiftY", "Сдвиг по Y", "0"),
					],
					[], # Список переменных, которые вернет дополнение
					plugin_func, menu="<Image>/Multilayer/") # Имя исходной функции и меню, в которое будет помещён пункт, запускающий дополнение

main()