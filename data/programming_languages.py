dataset = {
    "programming_languages": {

        "python": [
            "def greet(name): return f'Hello, {name}!'",
            "numbers = [1,2,3]; squared = [x**2 for x in numbers]",
            "# Unicode test\nprint('Hello 世界')",
            "lambda x: x * 2"
        ],

        "javascript": [
            "function greet(name) { return `Hello, ${name}!`; }",
            "const nums = [1,2,3]; nums.map(x => x**2);",
            "console.log('Hello 🌍');",
            "let obj = {key: 'value'};"
        ],

        "cpp": [
            "#include <iostream>\nusing namespace std;",
            "int main(){ cout << 'Hello'; return 0; }",
            "vector<int> v = {1,2,3};",
            "auto x = 10;"
        ],

        "sql": [
            "SELECT * FROM users WHERE age > 25;",
            "INSERT INTO table VALUES (1, 'test');",
            "GROUP BY name HAVING COUNT(*) > 1;",
            "JOIN orders ON users.id = orders.user_id;"
        ],

        "bash": [
            "for file in *.txt; do echo $file; done",
            "grep -r 'pattern' .",
            "export PATH=$PATH:/usr/local/bin",
            "cat file.txt | sort | uniq"
        ],

        "systems": [
            "int main() { return 0; }",
            "printf(\"Hello World\\n\");",
            "char* str = \"test\";",
            "for(int i=0;i<10;i++){}"
        ],

        "javascript_typescript": [
            "const x = (a: number) => a * 2;",
            "async function fetchData() {}",
            "let obj = {a:1, b:2};",
            "console.log('test');"
        ],

        "java": [
            "public class Main { public static void main(String[] args) {} }",
            "int x = 10;",
            "System.out.println(\"Hello\");",
            "List<Integer> nums = new ArrayList<>();"
        ],

        "go": [
            "func main() { fmt.Println(\"Hello\") }",
            "var x int = 10",
            "for i := 0; i < 10; i++ {}",
            "defer fmt.Println(\"done\")"
        ],

        "rust": [
            "fn main() { println!(\"Hello\"); }",
            "let x: i32 = 5;",
            "let v = vec![1,2,3];",
            "match x { _ => {} }"
        ],

        "kotlin_swift": [
            "fun main() { println(\"Hello\") }",
            "let x = 10",
            "var name: String = \"AI\"",
            "if (x > 0) {}"
        ],

        "php_ruby": [
            "$var = 10;",
            "puts 'Hello'",
            "def method; end",
            "<?php echo 'test'; ?>"
        ],

        "functional": [
            "(define (square x) (* x x))",
            "(map (lambda (x) (* x x)) '(1 2 3))",
            "let f x = x * x",
            "fn x => x + 1"
        ],

        "shell": [
            "ls -la",
            "grep 'pattern' file",
            "export VAR=1",
            "cat file | sort"
        ],

        "web": [
            "<div class='test'>Hello</div>",
            "body { margin: 0; }",
            "fetch('/api')",
            "<script>alert('hi')</script>"
        ],

        "gpu_cuda": [
            "__global__ void kernel() {}",
            "threadIdx.x",
            "blockIdx.x",
            "cudaMalloc(&ptr, size);"
        ],

        "solidity": [
            "contract Test { uint x; }",
            "function set(uint _x) public {}",
            "msg.sender",
            "require(x > 0);"
        ]
    }
}