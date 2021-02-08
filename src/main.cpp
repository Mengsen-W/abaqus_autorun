/*
 * @Author: Mengsen.Wang
 * @Date: 2021-02-07 10:40:06
 * @Last Modified by: Mengsen.Wang
 * @Last Modified time: 2021-02-07 10:55:10
 */

// TODO
// 执行分析 and 得到结果 -- cmd_exec
// 寻找 inp and 清理垃圾

#include <cstdlib>
#include <filesystem>
#include <iostream>
#include <iterator>
#include <string>
#include <vector>

#include "threadpool.h"

using namespace std::experimental::filesystem::v1;

int cmd_exec(const char* command) { return system(command); }

// int find_file() {}

// int cleanup() {}
// using namespace std::experimental::filesystem::v1;

auto discoverFiles(std::filesystem::path start_path) {
  std::vector<std::string> extensions = {".py"};
  std::vector<std::string> files;
  for (const auto& path :
       std::filesystem::recursive_directory_iterator(start_path)) {
    if (std::find(extensions.begin(), extensions.end(),
                  path.path().extension()) != extensions.end()) {
      files.push_back(path.path().string());
    }
  }
  return files;
}
void test_thread_pool() {
  // create thread pool with 4 worker threads
  ThreadPool pool(4);

  // enqueue and store future
  for (int i = 0; i < 8; i++) {
    auto result = pool.enqueue(cmd_exec, "dir");
    result = pool.enqueue(cmd_exec, "echo hello");
    result = pool.enqueue(cmd_exec, "echo world");
    result = pool.enqueue(cmd_exec, "pause");
  }

  // get result from future
  // std::cout << result.get() << std::endl;
}

int main() {
  // auto files = discoverFiles(fs::current_path().root_path());
  // std::copy(files.begin(), files.end(),
  //           std::ostream_iterator<std::string>(std::cout, "\n"));
  return 0;
}