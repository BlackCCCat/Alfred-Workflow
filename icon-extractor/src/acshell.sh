#!/bin/bash

QUERY="$1"
ARG="$2"

###################################
## 1. LIST APPS TO EXTRACT ICONS ##
###################################

if [[ "$ARG" == "--start" ]]; then
	# 找到所有Applications路径下名为QUERY的所有app，不输入时找到全部app
	LIST=$(find /Applications -maxdepth 2 | egrep -i "\.app$" | grep -i "$QUERY")
	# 在Alfred展开菜单中显示在线搜索app的选项
	echo '<?xml version="1.0"?><items>
		<item>
			<arg>online^'$QUERY'</arg>
			<title>Search app icons online</title>
			<subtitle>Switch to online search in App Store and Mac App Store</subtitle>
		</item>'

	# 读取一个输入的app
	while IFS= read -r line
	do
	# 用basename命令把Applications/xxx.app提取为xxx.app，再用sed把.app后缀替换掉
	appnm=$(basename "$line" | sed 's|.app||g')
	# 在Alfred展开菜单中显示LIST中的每个app，title为app名称，图标为app图标（由于选定了icon type为fileicon，因此当参数为文件时，直接显示文件自身的图标）
	echo '<item>
			<arg>'$line'</arg>
			<title>'$appnm'</title>
			<icon type="fileicon">'$line'</icon>
		</item>'
	done <<< "$LIST"
	echo '</items>'

###################################
##     2. LIST ICONS TO FILE     ##
###################################

elif [[ "$ARG" == "--extract" ]]; then
	qr=$(echo "$QUERY" | awk -F'^' '{print $1}')
	argument=$(echo "$QUERY" | awk -F'^' '{print $2}')

	if [[ "$qr" == "online" ]]; then
		# osascript命令执行apple script
		osascript -e 'tell application id "com.runningwithcrayons.Alfred" to run trigger "online" in workflow "com.mcskrzypczak.extracticon" with argument "'"$argument"'"'
	elsexc
		# 获取info.plist中的app icon信息
		appicon=$($HOME/.pyenv/shims/python3 acpython.py "$QUERY/Contents/Info.plist" --local --icon)
		# 将上一步appicon变量中字符串里的'.icns'替换为''
		appicon=${appicon//.icns/}
		# 获取info.plist中的app name信息
		appname=$($HOME/.pyenv/shims/python3 acpython.py "$QUERY/Contents/Info.plist" --local --name)
		# 用sips命令转换图像格式
		sips -s format png "$QUERY/Contents/Resources/$appicon.icns" --out "$HOME/Desktop/$appname.png"

		osascript -e 'tell application id "com.runningwithcrayons.Alfred" to run trigger "notify" in workflow "com.mcskrzypczak.extracticon" with argument "'"$HOME/Desktop/$appname.png"'"'
	fi

###################################
##  3. DOWNLOAD ICON TO DESKTOP  ##
###################################

elif [[ "$ARG" == "--download" ]]; then
	IMGURL=$(echo "$QUERY" | awk -F'^' '{print $1}')
	IMGEXT=$(echo "$IMGURL" | awk -F'.' '{print $NF}') # NF是字段数目，所以$NF是分割以后最后一个字段的值
	APPNM=$(echo "$QUERY" | awk -F'^' '{print $2}')
	DEV=$(echo "$QUERY" | awk -F'^' '{print $3}')

	curl -o "$HOME/Desktop/$APPNM-$DEV.$IMGEXT" "$IMGURL"

	if [[ "$IMGEXT" == "jpg" ]] || [[ "$IMGEXT" == "jpeg" ]]; then
		sips -s format png "$HOME/Desktop/$APPNM-$DEV.$IMGEXT" --out "$HOME/Desktop/$APPNM-$DEV.png"
		rm "$HOME/Desktop/$APPNM-$DEV.$IMGEXT"
		IMGEXT="png"
	fi

	if [[ "$DEV" == "iOS" ]]; then
	    export PYTHONPATH='./libs/'
        export PATH="$HOME/.pyenv/shims:$HOME/.pyenv/bin:$PATH"
		# 调用mask.py处理图片
		python3 mask.py "$HOME/Desktop/$APPNM-$DEV.$IMGEXT"
		rm "$HOME/Desktop/$APPNM-$DEV.$IMGEXT"
		mv "$HOME/Desktop/$APPNM-$DEV".png.png "$HOME/Desktop/$APPNM-$DEV".png
	fi

fi
