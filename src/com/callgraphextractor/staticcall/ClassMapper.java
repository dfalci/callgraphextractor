package com.callgraphextractor.staticcall;

import java.util.Arrays;

import org.apache.bcel.classfile.Constant;
import org.apache.bcel.classfile.ConstantPool;
import org.apache.bcel.classfile.EmptyVisitor;
import org.apache.bcel.classfile.JavaClass;
import org.apache.bcel.classfile.Method;
import org.apache.bcel.generic.ConstantPoolGen;
import org.apache.bcel.generic.MethodGen;

public class ClassMapper extends EmptyVisitor {
    private JavaClass item;
    private ConstantPoolGen cpool;
    
    public ClassMapper(JavaClass item) {
        this.item = item;
        cpool = new ConstantPoolGen(item.getConstantPool());
        
    }

    public void visitJavaClass(JavaClass item) {
        item.getConstantPool().accept(this);
        final ClassMapper cMapper = this;
        Arrays.asList(item.getMethods()).forEach(m->{
        	m.accept(cMapper);
        });
        
    }

    public void visitConstantPool(ConstantPool constantPool) {
        for (int i = 0; i < constantPool.getLength(); i++) {
            Constant constant = constantPool.getConstant(i);
            if (constant == null)
                continue;
            
            //tag de mapeamento
            if (constant.getTag() == 7) {
                System.out.println("Class:" + this.item.getClassName() + " "+constantPool.constantToString(constant));
            }
        }
    }

    public void visitMethod(Method method) {
        new MethodMapper(new MethodGen(method, this.item.getClassName(), this.cpool), this.item).start();
    }

    public void execute() {
        visitJavaClass(this.item);
    }
}
