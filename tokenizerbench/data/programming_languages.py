programming_languages_short = {

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


programming_languages_full = {

    "python": [
        "def greet(name): return f'Hello, {name}!'",
        "numbers = [1,2,3]; squared = [x**2 for x in numbers]",
        "# Unicode test\nprint('Hello 世界')",
        "lambda x: x * 2",
        "import numpy as np; arr = np.array([1,2,3]); print(arr.mean())",
        "class MyClass:\n    def __init__(self, x):\n        self.x = x\n    def __repr__(self):\n        return f'MyClass({self.x})'",
        "with open('file.txt', 'r', encoding='utf-8') as f:\n    data = f.read()",
        "result = {k: v for k, v in zip(keys, values) if v is not None}",
        "@decorator\ndef func(a: int, b: str = 'default') -> list[int]:\n    \"\"\"Docstring.\"\"\"\n    pass",
        "async def fetch(url: str) -> dict:\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as r:\n            return await r.json()",
        "try:\n    result = risky_op()\nexcept (ValueError, TypeError) as e:\n    logger.error(f'Error: {e}')\nfinally:\n    cleanup()",
        "from typing import Generator\ndef fib() -> Generator[int, None, None]:\n    a, b = 0, 1\n    while True:\n        yield a\n        a, b = b, a + b",
        "df = pd.DataFrame({'col': [1,2,3]})\ndf['new'] = df['col'].apply(lambda x: x**2)\ndf.groupby('col').agg({'new': 'sum'})",
        "model = torch.nn.Sequential(\n    torch.nn.Linear(128, 64),\n    torch.nn.ReLU(),\n    torch.nn.Linear(64, 10)\n)",
        "re.sub(r'(?P<year>\\d{4})-(?P<month>\\d{2})', r'\\g<month>/\\g<year>', text)",
        "PATH = os.environ.get('PATH', '').split(os.pathsep)",
        "pickle.dumps(obj)  # serialize\nobj2 = pickle.loads(data)  # deserialize",
        "itertools.chain.from_iterable([[1,2],[3,4],[5]])",
        "collections.Counter('abracadabra').most_common(3)",
        "functools.reduce(lambda a, b: a + b, range(1, 101))",
    ],

    "javascript": [
        "function greet(name) { return `Hello, ${name}!`; }",
        "const nums = [1,2,3]; nums.map(x => x**2);",
        "console.log('Hello 🌍');",
        "let obj = {key: 'value'};",
        "const fetchData = async (url) => { const res = await fetch(url); return res.json(); };",
        "class Animal { constructor(name) { this.name = name; } speak() { return `${this.name} makes a sound.`; } }",
        "const { a, b, ...rest } = obj; const [first, ...others] = arr;",
        "Promise.all([fetch('/api/a'), fetch('/api/b')]).then(([a, b]) => [a.json(), b.json()]);",
        "const memoize = fn => { const cache = new Map(); return (...args) => { const key = JSON.stringify(args); return cache.has(key) ? cache.get(key) : cache.set(key, fn(...args)).get(key); }; };",
        "document.querySelectorAll('.btn').forEach(btn => btn.addEventListener('click', handleClick));",
        "const worker = new Worker('worker.js'); worker.postMessage({type: 'START', data});",
        "const handler = { get: (t, k) => k in t ? t[k] : `${k} not found` }; new Proxy(target, handler);",
        "Object.entries(obj).reduce((acc, [k, v]) => ({...acc, [k]: transform(v)}), {});",
        "const stream = fs.createReadStream('file.txt'); stream.pipe(zlib.createGzip()).pipe(fs.createWriteStream('file.gz'));",
        "Symbol.iterator; Symbol.asyncIterator; Symbol.toPrimitive; Symbol.hasInstance;",
        "WeakRef; FinalizationRegistry; BigInt(2n**53n); structuredClone(obj);",
        "import('./module.js').then(m => m.default());",
        "const [state, setState] = useState(0); useEffect(() => { document.title = state; }, [state]);",
        "queueMicrotask(() => {}); requestAnimationFrame(() => {}); requestIdleCallback(() => {});",
        "new URL('https://example.com/path?q=1#hash').searchParams.get('q');",
    ],

    "typescript": [
        "const x = (a: number) => a * 2;",
        "async function fetchData<T>(url: string): Promise<T> { const res = await fetch(url); return res.json() as T; }",
        "interface User { id: number; name: string; email?: string; }",
        "type Result<T, E = Error> = { ok: true; value: T } | { ok: false; error: E };",
        "enum Direction { Up = 'UP', Down = 'DOWN', Left = 'LEFT', Right = 'RIGHT' }",
        "type DeepReadonly<T> = { readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K] };",
        "function assertNever(x: never): never { throw new Error('Unexpected: ' + x); }",
        "const isString = (x: unknown): x is string => typeof x === 'string';",
        "class Stack<T> { #items: T[] = []; push(item: T): void { this.#items.push(item); } pop(): T | undefined { return this.#items.pop(); } }",
        "type Awaited<T> = T extends Promise<infer U> ? Awaited<U> : T;",
        "const record: Record<string, number[]> = {};",
        "satisfies operator: const config = { port: 3000 } satisfies Partial<Config>;",
        "declare module '*.svg' { const content: string; export default content; }",
        "namespace MyLib { export interface Options { debug?: boolean; } }",
        "type UnionToIntersection<U> = (U extends any ? (x: U) => void : never) extends (x: infer I) => void ? I : never;",
    ],

    "cpp": [
        "#include <iostream>\nusing namespace std;",
        "int main(){ cout << 'Hello'; return 0; }",
        "vector<int> v = {1,2,3};",
        "auto x = 10;",
        "template<typename T>\nT max(T a, T b) { return a > b ? a : b; }",
        "std::unique_ptr<MyClass> ptr = std::make_unique<MyClass>(args);",
        "#include <algorithm>\nstd::sort(v.begin(), v.end(), [](int a, int b){ return a > b; });",
        "std::unordered_map<std::string, int> freq;\nfor (const auto& [k, v] : freq) { /* C++17 structured bindings */ }",
        "constexpr int factorial(int n) { return n <= 1 ? 1 : n * factorial(n-1); }",
        "std::thread t([&data]{ process(data); }); t.join();",
        "std::mutex mtx;\nstd::lock_guard<std::mutex> lock(mtx);",
        "#include <concepts>\ntemplate<std::integral T>\nT add(T a, T b) { return a + b; }  // C++20 concepts",
        "std::ranges::filter_view even = nums | std::views::filter([](int x){ return x % 2 == 0; });",
        "[[nodiscard]] auto compute() -> std::expected<int, std::string>;  // C++23",
        "volatile sig_atomic_t running = 1;\nsignal(SIGINT, [](int){ running = 0; });",
        "__attribute__((aligned(64))) float weights[1024];",
        "asm volatile(\"lock; xaddl %0, %1\" : \"+r\"(val), \"+m\"(*ptr));",
        "std::string_view sv = \"hello\";\nstd::span<const int> sp{arr, len};",
        "co_await some_coroutine();  // C++20 coroutines",
        "std::format(\"{:>10.2f}\", 3.14);  // C++20 format",
    ],

    "rust": [
        "fn main() { println!(\"Hello\"); }",
        "let x: i32 = 5;",
        "let v = vec![1,2,3];",
        "match x { _ => {} }",
        "let result: Result<i32, String> = Ok(42);",
        "fn fibonacci(n: u64) -> u64 { match n { 0 => 0, 1 => 1, n => fibonacci(n-1) + fibonacci(n-2) } }",
        "impl<T: Display + PartialOrd> Pair<T> { fn cmp_display(&self) { if self.x >= self.y { println!(\"{}\", self.x); } } }",
        "let s = String::from(\"hello\");\nlet s2 = s;  // move semantics - s is no longer valid",
        "async fn fetch_url(url: &str) -> Result<String, reqwest::Error> { reqwest::get(url).await?.text().await }",
        "use std::sync::{Arc, Mutex};\nlet shared = Arc::new(Mutex::new(0));\nlet clone = Arc::clone(&shared);",
        "#[derive(Debug, Clone, Serialize, Deserialize)]\nstruct Config { host: String, port: u16 }",
        "trait Animal { fn name(&self) -> &str; fn speak(&self) -> String; }\nimpl Animal for Dog { fn name(&self) -> &str { &self.name } fn speak(&self) -> String { \"Woof!\".to_string() } }",
        "let evens: Vec<_> = (0..100).filter(|x| x % 2 == 0).collect();",
        "unsafe { let raw = Box::into_raw(boxed); *raw = 42; let _ = Box::from_raw(raw); }",
        "macro_rules! vec_of_strings { ($($x:expr),*) => { vec![$($x.to_string()),*] }; }",
        "use std::collections::HashMap;\nlet freq = text.chars().fold(HashMap::new(), |mut m, c| { *m.entry(c).or_insert(0) += 1; m });",
        "const BUFFER_SIZE: usize = 4096;\nstatic GLOBAL_CONFIG: OnceLock<Config> = OnceLock::new();",
        "pub mod api { pub(crate) fn internal() {} pub fn external() {} }",
        "type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;",
        "#[tokio::main]\nasync fn main() -> Result<()> { let listener = TcpListener::bind(\"0.0.0.0:8080\").await?; Ok(()) }",
    ],

    "go": [
        "func main() { fmt.Println(\"Hello\") }",
        "var x int = 10",
        "for i := 0; i < 10; i++ {}",
        "defer fmt.Println(\"done\")",
        "type Server struct { host string; port int }",
        "func (s *Server) Start() error { return http.ListenAndServe(fmt.Sprintf(\"%s:%d\", s.host, s.port), nil) }",
        "ch := make(chan int, 10)\ngo func() { ch <- compute() }()\nresult := <-ch",
        "ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)\ndefer cancel()",
        "var wg sync.WaitGroup\nfor _, item := range items { wg.Add(1); go func(i Item) { defer wg.Done(); process(i) }(item) }\nwg.Wait()",
        "interface{} any // Go 1.18+\nfunc Map[T, U any](s []T, f func(T) U) []U { result := make([]U, len(s)); for i, v := range s { result[i] = f(v) }; return result }",
        "if err := doSomething(); err != nil { return fmt.Errorf(\"doSomething: %w\", err) }",
        "select { case msg := <-ch1: handleMsg(msg); case <-time.After(timeout): handleTimeout(); case <-ctx.Done(): return ctx.Err() }",
        "http.HandleFunc(\"/api\", func(w http.ResponseWriter, r *http.Request) { json.NewEncoder(w).Encode(response) })",
        "type Option[T any] struct { value T; valid bool }\nfunc Some[T any](v T) Option[T] { return Option[T]{v, true} }",
        "//go:generate protoc --go_out=. service.proto\n//go:build linux && amd64",
        "_ = (*io.Reader)(nil)  // interface compliance check",
        "runtime.GOMAXPROCS(runtime.NumCPU())",
        "pprof.StartCPUProfile(f); defer pprof.StopCPUProfile()",
        "reflect.TypeOf(x).Kind() == reflect.Ptr",
        "sync/atomic: atomic.AddInt64(&counter, 1)",
    ],

    "java": [
        "public class Main { public static void main(String[] args) {} }",
        "int x = 10;",
        "System.out.println(\"Hello\");",
        "List<Integer> nums = new ArrayList<>();",
        "record Point(int x, int y) {}  // Java 16+",
        "var list = new ArrayList<String>();  // Java 10+ type inference",
        "Stream.of(1,2,3,4,5).filter(n -> n % 2 == 0).map(n -> n * n).collect(Collectors.toList());",
        "Optional<String> opt = Optional.ofNullable(str).filter(s -> !s.isEmpty()).map(String::toUpperCase);",
        "@FunctionalInterface interface Transformer<T, R> { R transform(T input); }",
        "sealed interface Shape permits Circle, Rectangle, Triangle {}  // Java 17+",
        "switch (obj) { case String s -> s.length(); case Integer i -> i; default -> 0; }  // Pattern matching Java 21",
        "CompletableFuture.supplyAsync(() -> compute()).thenApply(r -> transform(r)).exceptionally(Throwable::getMessage);",
        "@SpringBootApplication\npublic class App { public static void main(String[] a) { SpringApplication.run(App.class, a); } }",
        "synchronized (lock) { while (!ready) lock.wait(); }",
        "try (var conn = DriverManager.getConnection(url); var stmt = conn.prepareStatement(sql)) { stmt.executeUpdate(); }",
        "Map<String, Long> freq = words.stream().collect(Collectors.groupingBy(w -> w, Collectors.counting()));",
        "interface Validator<T> { boolean validate(T t); default Validator<T> and(Validator<T> other) { return t -> validate(t) && other.validate(t); } }",
        "StackWalker.getInstance().walk(frames -> frames.limit(5).collect(Collectors.toList()));",
        "VarHandle handle = MethodHandles.lookup().findVarHandle(MyClass.class, \"field\", int.class);",
        "Executors.newVirtualThreadPerTaskExecutor()  // Java 21 virtual threads",
    ],

    "python_ml": [
        "model = transformers.AutoModelForCausalLM.from_pretrained('gpt2', torch_dtype=torch.float16)",
        "tokenizer = transformers.AutoTokenizer.from_pretrained('bert-base-multilingual-cased')",
        "inputs = tokenizer(texts, padding=True, truncation=True, return_tensors='pt', max_length=512)",
        "loss = F.cross_entropy(logits.view(-1, vocab_size), labels.view(-1), ignore_index=-100)",
        "optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5, weight_decay=0.01)",
        "scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=100, num_training_steps=1000)",
        "with torch.cuda.amp.autocast():\n    output = model(**inputs)\n    loss = output.loss",
        "torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)",
        "accelerator = Accelerate(); model, optimizer, dataloader = accelerator.prepare(model, optimizer, dataloader)",
        "dataset = datasets.load_dataset('wikitext', 'wikitext-103-v1', split='train')",
    ],

    "sql": [
        "SELECT * FROM users WHERE age > 25;",
        "INSERT INTO table VALUES (1, 'test');",
        "GROUP BY name HAVING COUNT(*) > 1;",
        "JOIN orders ON users.id = orders.user_id;",
        "WITH cte AS (SELECT id, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) rn FROM employees) SELECT * FROM cte WHERE rn = 1;",
        "SELECT COALESCE(name, 'Unknown'), NULLIF(score, 0), IIF(active=1, 'Yes', 'No') FROM records;",
        "CREATE INDEX CONCURRENTLY idx_users_email ON users(email) WHERE deleted_at IS NULL;",
        "EXPLAIN ANALYZE SELECT /*+ INDEX(u idx_email) */ * FROM users u WHERE u.email = $1;",
        "UPDATE users SET last_login = NOW(), login_count = login_count + 1 WHERE id = $1 RETURNING *;",
        "SELECT jsonb_agg(data), jsonb_build_object('key', value) FROM logs WHERE ts > NOW() - INTERVAL '1 hour';",
        "COPY users FROM STDIN WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');",
        "SELECT * FROM events WHERE ts BETWEEN SYMMETRIC '2024-01-01' AND '2024-12-31';",
        "CREATE MATERIALIZED VIEW monthly_stats AS SELECT DATE_TRUNC('month', ts), COUNT(*) FROM events GROUP BY 1;",
        "SELECT array_agg(DISTINCT tag ORDER BY tag), string_agg(name, ', ') FROM products GROUP BY category;",
        "DELETE FROM old_data USING new_data WHERE old_data.id = new_data.id AND old_data.version < new_data.version;",
    ],

    "bash": [
        "for file in *.txt; do echo $file; done",
        "grep -r 'pattern' .",
        "export PATH=$PATH:/usr/local/bin",
        "cat file.txt | sort | uniq",
        "find . -name '*.py' -newer requirements.txt -exec wc -l {} +",
        "jq '.users[] | select(.active == true) | .email' users.json | sort -u",
        "awk 'NR>1 {sum+=$3; count++} END {print sum/count}' data.csv",
        "sed -i 's/old_string/new_string/g; /^#/d; /^$/d' config.txt",
        "declare -A map; while IFS='=' read -r k v; do map[$k]=$v; done < config",
        "set -euo pipefail; trap 'cleanup' EXIT INT TERM",
        "parallel -j4 'ffmpeg -i {} -c:a libmp3lame {.}.mp3' ::: *.wav",
        "watch -n1 'docker stats --no-stream | sort -k3 -rh | head -10'",
        "rsync -avz --delete --exclude='.git' src/ user@host:dst/",
        "openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes",
        "systemctl list-units --state=failed --type=service | awk '{print $1}'",
    ],

    "web": [
        "<div class='container' aria-label='Main content' role='main'>\n  <h1>Hello</h1>\n  <p class='text-muted'>World</p>\n</div>",
        "body { margin: 0; font-family: system-ui, -apple-system, sans-serif; --primary: #007bff; }",
        "@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }",
        "@media (prefers-color-scheme: dark) { :root { --bg: #1a1a1a; --fg: #e0e0e0; } }",
        "fetch('/api/data', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) })",
        "const observer = new IntersectionObserver(entries => entries.forEach(e => e.target.classList.toggle('visible', e.isIntersecting)));",
        "<template id='tmpl'><slot name='content'></slot></template>\ncustomElements.define('my-el', class extends HTMLElement { constructor() { super(); this.attachShadow({mode:'open'}); } });",
        "navigator.serviceWorker.register('/sw.js').then(reg => reg.pushManager.subscribe({userVisibleOnly: true}));",
        "const db = await indexedDB.open('mydb', 1);\ndb.createObjectStore('store', {keyPath: 'id', autoIncrement: true});",
        "import { createStore } from 'redux';\nconst store = createStore(reducer, composeWithDevTools(applyMiddleware(thunk)));",
    ],

    "gpu_cuda": [
        "__global__ void kernel() {}",
        "threadIdx.x",
        "blockIdx.x",
        "cudaMalloc(&ptr, size);",
        "__global__ void matMul(float* A, float* B, float* C, int N) {\n  int row = blockIdx.y * blockDim.y + threadIdx.y;\n  int col = blockIdx.x * blockDim.x + threadIdx.x;\n  float sum = 0.0f;\n  for (int k = 0; k < N; k++) sum += A[row*N+k] * B[k*N+col];\n  C[row*N+col] = sum;\n}",
        "__shared__ float tile[TILE_SIZE][TILE_SIZE];\n__syncthreads();",
        "cudaMemcpyAsync(dst, src, size, cudaMemcpyDeviceToDevice, stream);",
        "cublasGemmEx(handle, CUBLAS_OP_N, CUBLAS_OP_N, M, N, K, &alpha, A, CUDA_R_16F, ...);",
        "#pragma omp target teams distribute parallel for\nfor (int i = 0; i < N; i++) { c[i] = a[i] + b[i]; }",
        "thrust::device_vector<int> d_vec(h_vec.begin(), h_vec.end());\nthrust::sort(d_vec.begin(), d_vec.end());",
    ],

    "functional": [
        "(define (square x) (* x x))",
        "(map (lambda (x) (* x x)) '(1 2 3))",
        "let f x = x * x",
        "fn x => x + 1",
        "-- Haskell\nfib :: Integer -> Integer\nfib 0 = 0\nfib 1 = 1\nfib n = fib (n-1) + fib (n-2)",
        "-- Haskell type class\nclass Functor f where\n  fmap :: (a -> b) -> f a -> f b",
        "(* OCaml *)\nlet rec fold_left f acc = function\n  | [] -> acc\n  | x :: xs -> fold_left f (f acc x) xs",
        "; Clojure\n(defn memoize [f]\n  (let [cache (atom {})]\n    (fn [& args]\n      (if-let [v (get @cache args)]\n        v\n        (let [result (apply f args)]\n          (swap! cache assoc args result)\n          result)))))",
        "-- Elm\ntype Msg = Increment | Decrement\nupdate : Msg -> Model -> Model\nupdate msg model =\n  case msg of\n    Increment -> model + 1\n    Decrement -> model - 1",
        "-- PureScript\nforeign import data Effect :: Type -> Type\nmain :: Effect Unit\nmain = log \"Hello, PureScript!\"",
    ],

    "solidity": [
        "contract Test { uint x; }",
        "function set(uint _x) public {}",
        "msg.sender",
        "require(x > 0);",
        "// SPDX-License-Identifier: MIT\npragma solidity ^0.8.19;\n\ncontract ERC20 {\n    mapping(address => uint256) public balanceOf;\n    event Transfer(address indexed from, address indexed to, uint256 value);\n}",
        "modifier onlyOwner() { require(msg.sender == owner, \"Not owner\"); _; }",
        "function safeTransfer(IERC20 token, address to, uint256 amount) internal { require(token.transfer(to, amount), \"Transfer failed\"); }",
        "assembly { let result := call(gas(), addr, value, dataOffset, dataLength, 0, 0) }",
        "error InsufficientBalance(uint256 available, uint256 required);\nrevert InsufficientBalance(balance, amount);",
        "bytes32 private constant DOMAIN_SEPARATOR = keccak256(abi.encode(TYPE_HASH, NAME_HASH, VERSION_HASH, block.chainid, address(this)));",
    ],

    "shell_scripting": [
        "ls -la",
        "grep 'pattern' file",
        "export VAR=1",
        "cat file | sort",
        "#!/usr/bin/env bash\nset -euo pipefail\nIFS=$'\\n\\t'",
        "[ -f \"$file\" ] && echo exists || echo missing",
        "$(command -v python3 || command -v python)",
        "curl -fsSL https://example.com | bash -s -- --option value",
        "2>&1 | tee -a /var/log/app.log",
        "nohup python server.py > /dev/null 2>&1 &",
    ],

    "kotlin_swift": [
        "fun main() { println(\"Hello\") }",
        "let x = 10",
        "var name: String = \"AI\"",
        "if (x > 0) {}",
        "// Kotlin coroutines\nrunBlocking { launch { delay(1000L); println(\"World\") }; println(\"Hello\") }",
        "// Kotlin data class\ndata class User(val id: Int, val name: String, val email: String? = null)",
        "// Kotlin extension function\nfun String.isPalindrome() = this == this.reversed()",
        "// Swift async/await\nfunc fetchUser(id: Int) async throws -> User { let (data, _) = try await URLSession.shared.data(from: url); return try JSONDecoder().decode(User.self, from: data) }",
        "// Swift property wrapper\n@propertyWrapper struct Clamped<T: Comparable> { var value: T; let range: ClosedRange<T>; var wrappedValue: T { get { value } set { value = min(max(range.lowerBound, newValue), range.upperBound) } } }",
        "// Kotlin sealed class\nsealed class Result<out T> { data class Success<T>(val data: T) : Result<T>(); data class Error(val message: String) : Result<Nothing>() }",
    ],

    "php_ruby": [
        "$var = 10;",
        "puts 'Hello'",
        "def method; end",
        "<?php echo 'test'; ?>",
        "<?php\nnamespace App\\Http\\Controllers;\nuse Illuminate\\Http\\Request;\nclass UserController extends Controller { public function index(Request $r) { return User::paginate(20); } }",
        "# Ruby: frozen_string_literal: true\nmodule MyGem\n  class Error < StandardError; end\n  def self.configure(&block)\n    yield Config.instance\n  end\nend",
        "<?php\n$result = array_map(fn($x) => $x ** 2, array_filter($nums, fn($x) => $x % 2 === 0));",
        "# Ruby metaprogramming\nclass MyClass\n  attr_reader :name\n  define_method(:greet) { |n| \"Hello, #{n}!\" }\nend",
        "<?php\n$pdo = new PDO($dsn, $user, $pass);\n$stmt = $pdo->prepare('SELECT * FROM users WHERE id = :id');\n$stmt->execute([':id' => $id]);",
        "# Ruby blocks/procs/lambdas\ndouble = ->(x) { x * 2 }\n[1,2,3].map(&double)",
    ],
}
