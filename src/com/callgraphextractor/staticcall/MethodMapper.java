package com.callgraphextractor.staticcall;

import org.apache.bcel.classfile.JavaClass;
import org.apache.bcel.generic.ConstantPoolGen;
import org.apache.bcel.generic.ConstantPushInstruction;
import org.apache.bcel.generic.EmptyVisitor;
import org.apache.bcel.generic.INVOKEINTERFACE;
import org.apache.bcel.generic.INVOKESPECIAL;
import org.apache.bcel.generic.INVOKESTATIC;
import org.apache.bcel.generic.INVOKEVIRTUAL;
import org.apache.bcel.generic.Instruction;
import org.apache.bcel.generic.InstructionConstants;
import org.apache.bcel.generic.InstructionHandle;
import org.apache.bcel.generic.MethodGen;
import org.apache.bcel.generic.ReturnInstruction;

public class MethodMapper extends EmptyVisitor {

    JavaClass originalClass;
    private MethodGen methodGenerator;
    private ConstantPoolGen cpool;
    private String print;

    public MethodMapper(MethodGen methodGenerator, JavaClass originalClass) {
        this.originalClass= originalClass;
        this.methodGenerator = methodGenerator;
        this.cpool = this.methodGenerator.getConstantPool();
        this.print = "M:" + this.originalClass.getClassName() + ":" + this.methodGenerator.getName() + " " + "(%s)%s:%s";
    }

    public void start() {
        if (this.methodGenerator.isAbstract() || this.methodGenerator.isNative())
            return;
        //itera nas instruções do class
        InstructionHandle instructionHandler = methodGenerator.getInstructionList().getStart();
        while (instructionHandler!= null){
        	Instruction ins = instructionHandler.getInstruction();
        	if (!visitInstruction(ins))
                ins.accept(this);
        	instructionHandler = instructionHandler.getNext();
        }
    }

    private boolean visitInstruction(Instruction ins) {
        short opcode = ins.getOpcode();//lembrar de checar o range das instruções aqui depois
        return ((InstructionConstants.INSTRUCTIONS[opcode] != null) && !(ins instanceof ConstantPushInstruction) && !(ins instanceof ReturnInstruction));
    }

    /**
     * indica acesso a um método
     */
    @Override
    public void visitINVOKEVIRTUAL(INVOKEVIRTUAL ins) {
        System.out.println(String.format(this.print, "M", ins.getReferenceType(this.cpool), ins.getMethodName(this.cpool)));
    }

    /**
     * Acesso à interfaces
     */
    @Override
    public void visitINVOKEINTERFACE(INVOKEINTERFACE ins) {
        System.out.println(String.format(this.print,"I", ins.getReferenceType(this.cpool), ins.getMethodName(this.cpool)));
    }

    /**
     * Acesso a objeto
     */
    @Override
    public void visitINVOKESPECIAL(INVOKESPECIAL ins) {
        System.out.println(String.format(this.print,"O", ins.getReferenceType(this.cpool), ins.getMethodName(this.cpool)));
    }

    /**
     * Acesso estático 
     */
    @Override
    public void visitINVOKESTATIC(INVOKESTATIC ins) {
        System.out.println(String.format(this.print,"S", ins.getReferenceType(this.cpool), ins.getMethodName(this.cpool)));
    }
}

