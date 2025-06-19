#!/bin/sh

X='{
  "branch":"main",
  "head_commit_id":"d72059a03639952d0244f4370545a38e2d3bf599",
  "id":3245570439353956,
  "path":"/Users/jordan.m.young0@gmail.com/pytorch-template.git",
  "provider":"gitHub",
  "url":"https://github.com/Jordan-M-Young/pytorch-template.git"
}'

GIT_FOLDER_ID=$(echo $X | jq '.id')


echo $GIT_FOLDER_ID " YO"