function load() {
circle = "<circle cx='50' cy='50' r='40' id='node1'/>";
document.getElementById('pane').innerHTML += circle;
circle = "<circle cx='50' cy='50' r='40' id='node2'/>";
document.getElementById('pane').innerHTML += circle;
element1 = document.getElementById('node1');
element2 = document.getElementById('node2');
console.log(element1);
rect1 = element1.getBoundingClientRect();
rect2 = element2.getBoundingClientRect();
console.log(rect2);
console.log(document.body.textContent);
line = "<line x1='0' y1='0' x2='200' y2='200'/>";
document.getElementById('pane').innerHTML += line;
}