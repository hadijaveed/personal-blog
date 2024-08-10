---
authors:
    - hjaveed
hide:
    - toc
date: 2016-10-18
readtime: 4
slug: writing-reactive-templates-with-handlebarsjs
---

# Writing reactive templates with HandlebarsJs.

The JavaScript community is going through the phase of evolution. There are so many frameworks, techniques and ideas that have been going on. It is really exciting but keeping up with it all is really a hard thing to do.
<!-- more -->

I started using Meteor on my first job. I was in love with Meteor because of two reasons.

1. A strong boilerplate. (You don’t have to worry about configurations).
2. It provides you reactivity out of the box. (Making Single page applications is fun with it).

Blaze in Meteor have a unique approach towards DOM. It keeps track of reactive dependencies by compiling html into something called htmljs which will only touch those parts of DOM that really needs to update instead of rendering the whole template. Read this article on [MeteorHacks](https://meteorhacks.com/how-blaze-works/).

Do I want to use Meteor or React every time ? What if I don’t have single page application like the one I am working on these days where we need to make small reusable components with rich client side interactions. I don’t want to use whole framework like Angular or a view layer like React for that. Because part of me miss the out of box reactivity in Meteor that maximizes the separation of concerns and code organisation. I decided to write a miniature library with Handlebars templates and to come up with a good way to integrate in our web application. The goal is to keep the data-flow plainly visible, making it easy to read and understand the code.

## Wait! Why do I need Reactive Programming ?
The best way to understand reactive programming is to compare it with event-driven programming. You use event-driven programming every time when you write a JavaScript app. Consider this JQuery event.

```js
$('div[name="some"]').on('click', () => {
    console.log('div have been clicked !');
});
```
This div will react every time someone clicks over it with a console log.

How about if I can have reactive data object that I am passing to the template. When your direct multiple (or single) variable value changes it should trigger a callback to observe it and update it’s value in the DOM. That can be done through reactive programming primitives. With the approach of reactive programming I can have these benefits.

1. Updating variables will update their values where used in DOM.
2. Maximizing separation of concern and providing clean and declarative way of organizing the code. (Will have no more spaghetti code with the all the changes nested under JQuery’s listeners callbacks).
3. Observing the data passed to the template through observers. (If the listeners are set on object keys that are passed to the template).
4. Abstraction over asynchronous HTTP calls by setting promises to the templates.

If I set key of the object that I am passing as a data to the template it should update the DOM in real time and run observer callbacks if the observers are set to this data object’s key.

```js
// updates the DOM as well
ReactiveHbs.set('counter', counter.get() + 1);
// Observer
ReactiveHbs.reactOnChange('counter', { debounce: 1000 }, (tpl) => {
    console.log( 'counter have been changed ' );
    console.log( 'value', tpl.get('counter') );        
});
```

So basically the set method generates all these changes. Since the Lodash is heavily concentrated on performance I am using Lodash for get and set methods.

### Optimal ways to update DOM.

After going through a lot of articles I found that these can be the optimal ways to update the DOM on change.

1. Keeping the DOM depth small.
2. Working with elements without appending to the DOM, and then just append everything together once everything is set up. (i.e using doc-fragments or strings).

With handlebars changes will always be off-DOM. Compile it on change and then append it to DOM. So upon change there will be only single DOM manipulation.

Since I am not using any virtual-DOM to diff the changes compiling template again and appending to DOM will be an expensive method on every change. But like I said this approach can be good with small templates or when your whole application is not a single page application and you don’t want to use any large front-end framework. On every compilation I use JQuery empty() method to avoid memory leaks which removes other constructs such as data and event handlers from the child elements before removing the elements themselves.

### Helpers
Instead of using global handlebars helpers bind helpers to only one template with the helper function.

```js
// bind helpers to only one template
ReactiveHbs.helpers({
    add(x, y) {
        return x + y;
    }
});
```

### Events
I really like the way you can define events in BackboneJs or Meteor. I tried to use the same approach. These events will be delegated events with respect to the container.

```js
// bind delegated events
ReactiveHbs.events({
    'click button[type="submit"]': (e, elm, tpl) => {
        e.preventDefault();
        tpl.set('someData', $(elem).attr('data-text')); 
    }
});
```

The non-delegated events can be defined under onRendered callback. Which will be triggered once the template is compiled and is in the DOM.

```js

// non-delegated events
ReactiveHbs.onRendered(function() {
   let self = this;
   $('button[type="submit"]').on('click', (e) => {
       e.preventDefault();
       self.set('someData', $(elem).attr('data-text'));
   });
});
```

### Abstraction over async HTTP calls

I really like how you can separate your business logic in AngularJs by making factory methods that you can inject into your controllers. For the HTTP async calls you can define promises in an object and can use them in the template.

```js
ReactiveHbs.promises({
    getAllUsers() {
        return $.get('https://api.github.com/users');
    },
});
// usage
ReactiveHbs.executePromise('getAllUsers', (err, data) => {
    if ( !err ) console.log(data);
});
```

### Demos
So we have helpers and the events for the template. Lets play with it with a common counter example.

```js
let counter = new ReactiveHbs({
    container: '.mount',               // html template mount point
    template: '#tpl',                  // hadnlebars template
    data: {
      count: 0
    }
 
});
// Events
counter.events({
    'click [name="increment-count"]': (e, elm, tpl) => {
        tpl.set( 'count', tpl.get('count') + 1 );
    }
});
counter.render();
```

[Codepen to play with](https://codepen.io/hjaveed/embed/YGOoKX?)

Instead of making a regular main-stream todo example to show reactivity I tried to come up with Trello like task cards example.

[Trello like Codepen to play with](https://codepen.io/hjaveed/embed/edLwRX?)

### Performance
I created a simple performance test with 10,000 item list and a reverse button. Hitting the reverse button renders the template again with a reverse list. On my machine the render time on average is 360ms which is pretty nice as compare to AngularJs which takes on average 600ms to render. See this [codepen](https://codepen.io/hjaveed/pen/vXzoEW) for AngularJS.

Definitely Angular’s dirty checking algorithm performance on large templates will be better when you cannot afford to render templates again on every change.

[Reactive Handlebars Performance.](https://codepen.io/hjaveed/embed/xEaeBp?)

While clicking twice the reverse list button this is the Google Chrome’s timeline performance overview.

<img src="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*p2f8wKbm23tjqqVfWMlbcA.png" alt="Google Chrome's timeline performance overview" style="display: block; margin-left: auto; margin-right: auto;">

### Next Steps

See the [GitHub](https://github.com/hadijaveed/reactive-handlebars)

