package com.callgraphextractor.staticcall;

import java.io.IOException;
import java.util.Collections;
import java.util.jar.JarFile;

import org.apache.bcel.classfile.ClassParser;

public class CallGraphExtractor {
	
	public static void main(String[] args) throws Throwable{
		for (String file : args){
			try(JarFile f = new JarFile(file)){
				Collections.list(f.entries()).forEach((entry)->{
					//depois criar um mecanismo do tipo white list e black list de classes aqui
					if ((!entry.isDirectory() && entry.getName().endsWith(".class"))){
	                    ClassMapper cMapper;
						try {
							cMapper = new ClassMapper(new ClassParser(file ,entry.getName()).parse());
							cMapper.execute();
						} catch (Exception e) {
							//pau violento
							e.printStackTrace();
						}
					}
				});
			}catch(IOException e){
				e.printStackTrace();
			}catch(SecurityException ex){
				ex.printStackTrace();
			}
		}
	}
	
}