from inkex import NSS, Layer


def find_or_create_layer(svg, name):
    # find an existing layer or create a new layer
    # need import NSS and Layer from inkex 
    layer_name = 'Layer %s' % name
    path = '//svg:g[@inkscape:label="%s"]' % layer_name
    elements = svg.xpath(path, namespaces=NSS)
    if elements:
        layer = elements[0]
    else:
        layer = Layer.new(layer_name)
        svg.add(layer)
    return layer