# Draw_Arrowhead Extension Documentation

When we are working on a technical drawing, we only need to use arrowhead for 
dimension lines, make a note of something on the drawing. The `markers` element 
on the `Stroke style` dialog has a drawback that the marker element will extend 
beyond the tip of line. 

The Draw_Arrowhead extension is designed to overcome the drawback of the `markers` 
element. It will add an arrowhead path element and modify the existing line path 
element. This webpage has more information on the extension. 

[https://inkscapetutorial.org/arrowhead-extension.html](https://inkscapetutorial.org/arrowhead-extension.html)

To use the extension, we use the `Draw Bezier` tool to create a line on the drawing. 
The start point of the line is the `Start` option on the extension dialog, and the 
end point of the line is the `End` option.  You can also choose `Both` option which 
will draw two arrowheads on both ends of the line. 

The `length` option of the arrowhead refers to the offset length from the tip of 
line in pixel.  The `angle` specifies the angle in degrees between two edge 
lines of the triangle arrowhead. 

The extension also has two arrow styles build in.  One is the `Normal` style and 
the other is `Sharp` style. 

The extension also support a two segment line path, which is often used to 
mark something on a drawing. An example is shown in the below figure. When we 
select a two segment line, the extension will only add an arrowhead at the 
`Start` of the path. 





