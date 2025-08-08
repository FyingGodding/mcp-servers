const { spawn } = require('child_process');
const path = require('path');

// 获取当前目录下的 main.py 的完整路径
const pythonScriptPath = path.join(__dirname, 'main.py');

// 启动 Python 脚本
const pythonProcess = spawn('python', [pythonScriptPath]);

// 输出 Python 脚本的标准输出
pythonProcess.stdout.on('data', (data) => {
  console.log(`Python 输出: ${data}`);
});

// 输出 Python 脚本的错误输出
pythonProcess.stderr.on('data', (data) => {
  console.error(`Python 错误: ${data}`);
});

// Python 脚本退出时的处理
pythonProcess.on('close', (code) => {
  console.log(`Python 脚本退出，代码 ${code}`);
});

// 处理错误事件
pythonProcess.on('error', (err) => {
  console.error('启动 Python 脚本失败:', err);
});