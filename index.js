function load() {
circle = "<g><circle cx='50' cy='50' r='40' id='node1'/><text x='50' y='50'>node1</text></g>";
document.getElementById('pane').innerHTML += circle;
circle = "<g><circle cx='150' cy='50' r='40' id='node2'/><text x='150' y='50'>node2</text></g>";
document.getElementById('pane').innerHTML += circle;
element1 = document.getElementById('node1');
element2 = document.getElementById('node2');
console.log(element1);
rect1 = element1.getBoundingClientRect();
rect2 = element2.getBoundingClientRect();
console.log(rect2);
console.log(document.body.textContent);
line = "<g><line x1='0' y1='0' x2='200' y2='200'/></g><text x='100.0' y='95.0'>1</text>";
document.getElementById('pane').innerHTML += line;
}