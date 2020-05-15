// C++ program for B-Tree insertion 
#ifndef __BTREE_CPP
#define __BTREE_CPP
#include <iostream>
#include <typeinfo>
#include <stack>
#include <vector>
#include <tuple>

#include "btree.h"
using namespace std; 

Node::Node(){

	key = new int[DEG-1];

	value = NULL;
	children = new Node*[DEG];



	for (int i=0; i<DEG; i++)
	{
		children[i] = NULL;
	}
	size = 0;
	isLeaf = true;
}

BPlusTree::BPlusTree(int _m){
	DEG = _m+1;
	root = NULL;
}

string BPlusTree::display(){
	// Do not edit this function
	ss.str("");
	traverse(root);
	return ss.str();
}

void BPlusTree::traverse(Node* cursor){
	
	// Do not edit this function
	if(cursor!=NULL)
	{
		// cout << "Checkpoint 44 " << cursor->key[0] << endl;
		for(int i = 0; i < cursor->size; i++)
		{
			ss<<"{"<<cursor->key[i]<<"}";
		}
		ss<<" ";
		if(cursor->isLeaf != true)
		{
			for(int i = 0; i < cursor->size+1; i++)
			{
				traverse(cursor->children[i]);
			}
		}
	}
}
void insertInList(int k, int* list, int size)
{
	if (size==0)
	{
		list[0] = k;
		return;
	}
	int x;
	for (int i=0; i<size; i++)
	{
		x = list[i];
		if (k < x)
		{
			for (int j=size; j>i; j--)
			{
				list[j] =list[j-1];
			}
			list[i] = k;
			return; //OR BREAK
		}
	}
	list[size] = k;
}

void NewOverSizeList(int* old, int* New, int k)
{
	for (int i=0; i<DEG; i++)
	{
		New[i] = old[i];
	}
	insertInList(k, New, DEG-1);
	int midpt = DEG/2;
	for (int i=0; i<midpt; i++)
	{
		old[i] = New[i];
	}
	for(int i=midpt; i<DEG; i++)
	{
		old[i] = 0;
	}

}

void BPlusTree::insert(int k){
	// Your code here
	Node* ptr;
	if (!root){// IF THE TREE DOES NOT EXIST AS OF YET
//		cout <<"setting up first nodee yayay***\n";
		ptr = new Node;
		ptr->key[0] = k;
		root = ptr;
		ptr->size++;
		return;
		//JOB DONE SO RETURN
	}

	stack<Node*> parents;
	ptr = root;
	while (ptr->isLeaf == false){ //search for the leaf to insert value in
//		cout << "not leaf, so adding to stacc\n";
		parents.push(ptr);
		{
		////////	BUG HANDLING	////////
		if (ptr->key[0] == 0){
			cout << "buggggieee";
			return;
		}
		}
		if (k < ptr->key[0]){
			ptr = ptr->children[0];
		}
		else
		{
			for (int i= ptr->size; i>=0; i--)
			{
				if (ptr->children[i])
				{
					if (k >= ptr->key[i-1])
					{
						ptr = ptr->children[i];
						break;
					}
				}else{//(hopefully?) redundant bug handling
					cout <<" BUGGIEEIEIE this shant be\n";
				}
			}

		}
	}
	// Now we have list of parents, and have reached the specific leaf node
	// to insert shit in. Now let'ss gooo!

	if (ptr->size < DEG-1) //IF NODE NOT ALREADY FULL
	{
		insertInList(k, ptr->key, ptr->size);
		ptr->size++;
		return;
	}
	// SPLIT THE NODE INTO TWO
	{
//		cout << "Node is full\n";
		int* tempkeys = new int[DEG];
		NewOverSizeList(ptr->key, tempkeys, k);		//makes a copy of the list into tempkeys and inserts K
								//copies the first half from tempkey, resets the remaining to 0

		int midpt = DEG/2;

		ptr->size = midpt;

		Node *newNode = new Node;
		for(int i=midpt; i<DEG; i++)
		{
			insertInList(tempkeys[i], newNode->key, newNode->size);
			newNode->size++;
		}
		delete[] tempkeys;
		newNode->children[DEG-1] = ptr->children[DEG-1];
		ptr->children[DEG-1] = newNode;

		int newVal = newNode->key[0];

		bool finish = false;
		while (!finish)
		{
			if(parents.empty()) // new root will be created
			{
				Node *newRoot = new Node;
				newRoot->isLeaf = false;
				newRoot->key[0] = newVal;
				newRoot->size++;
				newRoot->children[0] = root;
				newRoot->children[1] = newNode;
				root = newRoot;
				return;
			}else{
				Node *p = parents.top();
				parents.pop();
				if (p->size < DEG-1)
				{
					p->key[p->size] = newVal;
					p->children[p->size+1] = newNode;
					p->size++;
					return;
				}
				else
				{
					Node *newParent = new Node;
					//THIS SHOULD BE REDUNDANT BUT IS NOT?????
					for (int i=0; i<DEG; i++)
					{
						newParent->key[i] = 0;
					}

					//	ADJUST KEYS
					int* tempkeys = new int[DEG];
					NewOverSizeList(p->key, tempkeys, newVal);
					// for (int i=0; i<DEG; i++)
					// {
					// 	cout <<p->key[i] << "--" << endl; //<< newParent->key[i] << "--" << newVal << endl;
					// }
					// for (int i=0; i<DEG; i++)
					// {
					// 	cout <<tempkeys[i] << "--" ;// << endl; //<< newParent->key[i] << "--" << newVal << endl;
					// }
					// cout  <<"\n#### " << DEG << endl << endl;

					int midpt = DEG/2;
					p->size = midpt;
					newParent->isLeaf = false;
					for(int i=midpt+1; i<DEG; i++)
					{
//						cout <<">" << tempkeys[i] << endl; 
						insertInList(tempkeys[i], newParent->key, newParent->size);
						newParent->size++;
					}

					//	ADJUST POINTERS
					Node **tempChildren = new Node*[DEG +1];
					int j = 0;
					for (int i=0; i<DEG; i++)
					{
//						int j=i;
						tempChildren[j] = p->children[i];
						if (tempkeys[i] == newVal)
						{
//							cout <<"BAZINGA";
							j++;
							tempChildren[j] = newNode;
						}
						j++;
					}
					if (j !=  DEG+1)
					{
//						cout <<" MAJORR UGGIES" << j << endl;
					}


					for (int i=0; i<=midpt; i++)
					{
						p->children[i] = tempChildren[i];
					}
					for (int i=midpt+1; i<DEG; i++)
					{
						p->children[i] = NULL;
					}
					j=0;
					for (int i=midpt+1; i<=DEG; i++)
					{
						newParent->children[j] = tempChildren[i];
						j++;
					}
					for (j=j; j<DEG; j++)
					{
						newParent->children[j] = NULL;
					}
					newNode = newParent;
					newVal = tempkeys[midpt];

					delete[] tempkeys;
					delete[] tempChildren;
				}
			}
		}
	}


}

Node* BPlusTree::search(int k){
	if (!root)
	{
		return NULL;
	}
	Node *ptr = root;
	while (ptr->isLeaf == false)
	{
		if (k < ptr->key[0]){
			ptr = ptr->children[0];
		}
		else
		{
			for (int i= ptr->size; i>=0; i--)
			{
				if (ptr->children[i])
				{
					if (k >= ptr->key[i-1])
					{
						ptr = ptr->children[i];
						break;
					}
				}else{//(hopefully?) redundant bug handling
					cout <<" BUGGIEEIEIE this shant be\n";
				}
			}

		}
	}
	for (int i=0; i<ptr->size; i++)
	{
		if (k == ptr->key[i])
		{
			return ptr;
		}
	}
	return NULL;
}
Node* BPlusTree::findParent(Node* ptr, Node* child)
{
	Node* parent;
	if(ptr->isLeaf)
	{
		return NULL;
	}
	if((ptr->children[0])->isLeaf)
	{
		return NULL;
	}
	int i = 0;
	while(i<ptr->size+1)
	{
		if(ptr->children[i]!=child)
		{
			parent = findParent(ptr->children[i],child);
		}
		else
		{
			parent = ptr;
			return parent;
		}
		i++;
	}

	return parent;
}


void BPlusTree::remove(int k){
	// Your code here
	Node* ptr = root;
	if (root == NULL)
	{
		return;
	}
	stack<Node*> parents;
	while (ptr->isLeaf == false){ //search for the leaf to insert value in
//		cout << "not leaf, so adding to stacc\n";
		parents.push(ptr);
		{
		////////	BUG HANDLING	////////
		if (ptr->key[0] == 0){
			cout << "buggggieee";
			return;
		}
		}
		if (k < ptr->key[0]){
			ptr = ptr->children[0];
		}
		else
		{
			for (int i= ptr->size; i>=0; i--)
			{
				if (ptr->children[i])
				{
					if (k >= ptr->key[i-1])
					{
						ptr = ptr->children[i];
						break;
					}
				}else{//(hopefully?) redundant bug handling
					cout <<" BUGGIEEIEIE this shant be\n";
				}
			}

		}
	}
} 


// int main()
// {
// 	cout << "wooah" << endl;
// 	BPlusTree tree1();
// 	tree1.insert(1); 
// 	tree1.insert(5); 
// 	tree1.insert(9);
// 	tree1.insert(10);
// 	tree1.insert(11);
// 	tree1.insert(14);
// 	tree1.insert(15);
// 	tree1.insert(16);
// 	tree1.insert(21);
// 	tree1.insert(32);
// 	cout << tree1.display() << endl;
// 	// string output = tree1.display();
// 	// string expected = "{15} {9}{11} {1}{5} {9}{10} {11}{14} {21} {15}{16} {21}{32} ";
// //	cout << endl << output << endl << expected << endl;

// 	// BPlusTree tree2(4);
// 	// tree2.insert(1); 
// 	// tree2.insert(2); 
// 	// tree2.insert(3); 
// 	// tree2.insert(4); 
// 	// tree2.insert(5);
// 	// tree2.insert(7);

// 	// cout << tree2.display() << endl;
// 	// tree2.insert(8);
// 	// tree2.insert(6);

// 	// cout << tree2.display() << endl;
// 	// int marks =0;
// 	// if (tree2.search(3) && tree2.search(7) && !tree2.search(12)){
// 	// 	cout << "Search correct" << endl;
// 	// 	marks+=20;
// 	// }
// 	// else
// 	// 	cout << "Search incorrect" << endl;

// 	// int * lol = new int[2900];
// 	// for (int i=0; i<2900; i++)
// 	// {
// 	// 	cout << lol[i] <<"->";
// 	// }

// 	return 0;
// }
#endif