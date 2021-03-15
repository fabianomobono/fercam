


const styles = {
  fontFamily: 'sans-serif',
  testAllign: 'center',
}

let id = 0;

const Todo = props => (
  <li>
    <input type="checkbox" checked={props.todo.checked} onChange={props.onToggle}/>
    <button onClick={props.onDelete}>Delete</button>
    <span>{props.todo.text}</span>
  </li>
)

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      todos: [],
    }
  }

  addTodo() {
    const text = prompt("Add TODO text please!")
    if (text != null && text !== ''){
      this.setState({
        todos: [...this.state.todos, {key: id++, text: text, checked: false}],
      })
    }
  }

  removeTodo(id) {
    this.setState({
      todos: this.state.todos.filter(todo => todo.key !== id)
    })
  }

  toggleTodo(id) {
    this.setState({
      todos: this.state.todos.map(todo => {
          if (todo.key !== id) return todo
          return {
            key: todo.key,
            text: todo.text,
            checked: !todo.checked,
          }
      })
    })
  }

  render () {
    return (
      <div>
        <div> Todo count: {this.state.todos.length}</div>
        <div> Unchecked count: {this.state.todos.filter(x => x.checked === true).length}</div>
        <button onClick={() => this.addTodo()} >Add Todo</button>
        <ul>
          {this.state.todos.map(todo => <Todo
            onToggle={() => this.toggleTodo(todo.key)}
            onDelete={() => this.removeTodo(todo.key)}
            todo={todo}
            key={todo.key}/> )}
        </ul>
      </div>
    )
  }
}

ReactDOM.render(
  <App />,
  document.getElementById('root')
);
