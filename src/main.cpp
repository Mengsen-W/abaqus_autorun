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
#include <functional>

#include "threadpool.h"

int cmd_exec(int a) { return a; }

// int find_file() {}

// int cleanup() {}
// using namespace std::experimental::filesystem::v1;

// auto discoverFiles(std::filesystem::path start_path) {
//   std::vector<std::string> extensions = {".py"};
//   std::vector<std::string> files;
//   for (const auto& path :
//        std::filesystem::recursive_directory_iterator(start_path)) {
//     if (std::find(extensions.begin(), extensions.end(),
//                   path.path().extension()) != extensions.end()) {
//       files.push_back(path.path().string());
//     }
//   }
//   return files;
// }
void test_thread_pool() {
  // create thread pool with 4 worker threads
  ThreadPool pool(4);

  auto result = pool.enqueue([](int answer) { return answer; }, 42);
  // get result from future
  std::cout << result.get() << std::endl;
}

int main() {
  std::cout << std::filesystem::current_path() << std::endl;
  // std::copy(files.begin(), files.end(),
  //           std::ostream_iterator<std::string>(std::cout, "\n"));
  return 0;
}