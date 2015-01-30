__author__ = 'Iva'
from dbnormalizer.core.table.Table import Table
from dbnormalizer.core.importdata.StrippedPartition import StrippedPartition
from dbnormalizer.core.importdata.CandidateInfo import CandidateInfo


class FDDetection:
    def __init__(self, engine, schema_name, table):
        self.engine = engine
        self.table = table
        self.schema_name = schema_name
        self.table_full_name = self.schema_name + "." + str(table.name)
        self.partitions = []
        self.last_level = []
        self.currant_level = []


    def setup_table(self):
        conn = self.engine.connect()
        partitions=[]
        attr_list = self.table.get_attribute_string_list()
        for column in attr_list:
            res = conn.execute("select " + column + " from " + self.table_full_name + " order by " + attr_list[0])
            if res:
                partition = StrippedPartition(column, res)
                self.partitions.append(partition)
        return self.partitions

    def get_partition_column(self, column):
        for part in self.partitions:
            if part.column == column:
                return part


    def get_data(self):
        connection = self.engine.connect()
        result = connection.execute("select * from " + self.table_full_name)
        return result

    def get_FD(self):
        # level 0
        attributes = self.table.get_attribute_string_list()
        empty = []

        c = CandidateInfo(attributes, None)
        c.set_RHS(attributes)
        empty.append(c)
        self.last_level.append(empty)
        #level 1
        for column in attributes:
            candidate = {}
            candidate[column] = True
            sp = self.get_partition_column(column)
            c = CandidateInfo(attributes,sp)
        #sve kolone pune listu trenutnog nivoa

	#private HashMap<BitSet, CandidateInfo> current_level = null;
			# 	current_level.put(candidate, candidateInfo);
        #for candidates
            rhs = c.rhs_att
            import copy
            x_clone = copy.copy(candidate)

        #
		# for (BitSet X : current_level.keySet() ){
		# 	BitSet rhs = current_level.get(X).getRHS();
		# 	BitSet Xclone = (BitSet)X.clone();
		# 	//iterate through all bits in the attribute set
		# 	for (int l = X.nextSetBit(0); l >= 0; l = X.nextSetBit(l+1)) {
		# 		Xclone.clear(l);
		# 		BitSet CxwithouA = last_level.get(Xclone).getRHS();
		# 		rhs.and(CxwithouA);
		# 		Xclone.set(l);
		# 	}
		# 	CandidateInfo c = current_level.get(X);
		# 	c.setRHS(rhs);
		# 	current_level.put(X, c);
		# }
		# //--------------------COMPUTE DEPENDENCIES--------------------------->
		# //for each AttributeSet do
		# if(level > 1){
		# 	//BitSet that represents the Relationscheme
		#
		#
		# 	for (BitSet attribute : current_level.keySet() ){
		# 		//For each A in X intersec C(X) do
		# 		BitSet C = current_level.get(attribute).getRHS();
		# 		BitSet intersection = (BitSet)attribute.clone();
		#
		#
		# 		intersection.and(C);	//intersection X n C(X)
		#
		# 		//create a copy the attributeSet to avoid a ConcurrentModificationError
		# 		BitSet X = (BitSet) attribute.clone();
		#
		#
		# 		//go through all A in XnC(X)
		# 		for (int l = intersection.nextSetBit(0); l >= 0; l = intersection.nextSetBit(l+1)) {
		# 			X.clear(l);
		# 			boolean fd_holds = false;
		# 			//if the memory version of Tane-java ist used, Stripped Partitions are used
		#
		# 			StrippedPartition spXwithoutA = last_level.get(X).getStrippedPartition();
		# 			StrippedPartition spX = current_level.get(attribute).getStrippedPartition();
		# 			//check if FD holds or not
		# 			if(spX.error() == spXwithoutA.error()){
		# 				fd_holds = true;
		# 			}
		#
		# 			if(fd_holds){
		# 				foundFDs++;
		# 				//console output
		# 				if(debug)
		# 					System.out.println(X +" --> " +l);
		#





