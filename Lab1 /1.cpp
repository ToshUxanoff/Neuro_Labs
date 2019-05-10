#include <iostream>
#include <string>
#include <sstream>

using namespace std; 

// 
class Node 
{
public: 

// 
long long int key; 
// 
string value; 
// 
Node * parent; 
// 
Node * left; 
Node * right; 

Node ( long long int key, string value, Node * parent ); 

// 
bool add ( long long int key, string value ); 
// 
bool set ( long long int key, string value ); 
// 
bool remove ( long long int key ); 
// 
bool find ( long long int key, string & value ); 
// 
void maxDepth ( int n, int & max ); 
// 
void min ( long long int & key, string & value ); 
// 
void max ( long long int & key, string & value ); 
// 
void print ( int now, int goal ); 
// 
void clearAll (); 
};

Node::Node ( long long int key, string value, Node * parent )
{
this->key = key; 
this->value = value; 
this->parent = parent; 
left = 0; 
right = 0; 
}

// 
bool Node::add ( long long int key, string value )
{
// 
if ( key < this->key ) 
{
if ( left != 0 ) 
{
// , 
return left->add( key, value ); 
}
else
{
// , , 
left = new Node( key, value, this ); 
}
}
else if ( key == this->key )
{
// 
return false; 
}
else 
{
if ( right != 0 ) 
{
// , 
return right->add( key, value ); 
}
else
{
// , , 
right = new Node( key, value, this ); 
}
}

return true; 
}

// 
bool Node::set ( long long int key, string value )
{
// 
if ( key < this->key ) 
{
if ( left != 0 ) 
{
// , 
return left->set( key, value ); 
}
else
{
// 
return false; 
}
}
else if ( key == this->key )
{
// 
// 
this->value = value; 
return true; 
}
else 
{
if ( right != 0 ) 
{
// , 
return right->set( key, value ); 
}
else
{
// 
return false; 
}
}
}

// 
bool Node::remove ( long long int key )
{
// 
if ( key < this->key ) 
{
if ( left != 0 ) 
{
// , 
bool result = left->remove( key ); 
return result; 
}
else 
{
// 
return false; 
}
}
else if ( key == this->key )
{
// 
if ( left == 0 && right == 0 ) 
{
// 
// 
if ( parent != 0 ) 
{
if ( parent->left == this ) { parent->left = 0; }
else { parent->right = 0; }
}
// 
delete this; 

return true; 
}
else if ( left == 0 ) 
{
// 
// 
Node * exRight = right; 

this->key = exRight->key; 
this->value = exRight->value; 
this->left = exRight->left; 
this->right = exRight->right; 

if ( exRight->left != 0 ) { exRight->left->parent = this; }
if ( exRight->right != 0 ) { exRight->right->parent = this; }
delete exRight; 

return true; 
}
else if ( right == 0 ) 
{
// 
// 
Node * exLeft = left; 

this->key = exLeft->key; 
this->value = exLeft->value; 
this->left = exLeft->left; 
this->right = exLeft->right; 

if
( exLeft->left != 0 ) { exLeft->left->parent = this; }
if ( exLeft->right != 0 ) { exLeft->right->parent = this; }
delete exLeft; 

return true; 
}
else 
{
// 
if ( left->right == 0 ) 
{
// 
// 
Node * exLeft = left; 

this->key = exLeft->key; 
this->value = exLeft->value; 
this->left = exLeft->left; 

if ( exLeft->left != 0 ) { exLeft->left->parent = this; }
if ( exLeft->right != 0 ) { exLeft->right->parent = this; }
delete exLeft; 

return true; 
}
else 
{
// 
// 
Node * min = left->right; 
while ( min->right != 0 ) { min = min->right; } 

// 
this->key = min->key; 
this->value = min->value; 

// 
min->remove( min->key ); 

return true; 
}
}
}
else 
{
if ( right != 0 ) 
{
// , 
bool result = right->remove( key ); 
return result; 
}
else
{
// 
return false; 
}
}
}

// 
bool Node::find ( long long int key, string & value ) 
{
// 
if ( key < this->key ) 
{
if ( left != 0 ) 
{
// , 
bool result = left->find( key, value ); 
return result; 
}
else
{
// , 
return false; 
}
}
else if ( key == this->key )
{
// 
// 
value = this->value; 
return true; 
}
else 
{
if ( right != 0 ) 
{
// , 
bool result = right->find( key, value ); 
return result; 
}
else
{
// , 
return false; 
}
}
}

// 
void Node::maxDepth ( int n, int & max ) 
{
if ( n > max ) { max = n; } 

if ( left != 0 ) { left->maxDepth( n + 1, max ); }
if ( right != 0 ) { right->maxDepth( n + 1, max ); }
}

// 
void Node::min ( long long int & key, string & value ) 
{
if ( left != 0 ) 
{
// , 
left->min( key, value ); 
}
else
{
// 
key = this->key; 
value = this->value; 
}
}

// 
void Node::max ( long long int & key, string & value ) 
{
if ( right != 0 ) 
{
// , 
right->max( key, value ); 
}
else
{
// 
key = this->key; 
value = this->value; 
}
}

// 
void Node::print ( int now, int goal ) 
{
if ( now == goal ) 
{
if ( parent == 0 ) 
{
// 
cout « "[" « key « " " « value « "]"; 
} 
else 
{
// 
cout « "[" « key « " " « value « " " « parent->key « "] "; 
} 
}
else 
{
now++; 
if ( left != 0 ) 
{ 
left->print( now, goal ); 
}
else 
{
int d = goal - now; 
int n = 1; 
for ( int i = 0; i < d; i++ ) { n *= 2; } 
for ( int i = 0; i < n; i++ ) { cout « "_ "; }
}
if ( right != 0 ) 
{ 
right->print( now, goal ); 
}
else 
{
int d = goal - now; 
int n = 1; 
for ( int i = 0; i < d; i++ ) { n *= 2; } 
for ( int i = 0; i < n; i++ ) { cout « "_ "; }
}
now--; 
}
}

// 
void Node::clearAll () 
{
// 
if ( left != 0 ) { left->clearAll(); } 
if ( right != 0 ) { right->clearAll(); } 

left = 0; 
right = 0; 

delete this; 
}

// 
class Tree 
{
// 
Node * root; 

public: 

Tree (); 
~Tree (); 

// 
bool add ( long long int key, string value ); 
// 
bool set ( long long int key, string value ); 
// 
bool remove (
long long int key); 
// 
bool find ( long long int key, string & value ); 
// 
bool min ( long long int & key, string & value ); 
// 
bool max ( long long int & key, string & value ); 
// 
void print (); 
};

Tree::Tree() 
{
root = 0; 
}

Tree::~Tree() 
{
if ( root != 0 ) 
{
root->clearAll(); 
}
}

// 
bool Tree::add ( long long int key, string value ) 
{
if ( root == 0 ) 
{
// 
root = new Node( key, value, 0 ); 
return true; 
}
else 
{
// 
return root->add( key, value ); 
}
}

// 
bool Tree::set ( long long int key, string value ) 
{
if ( root == 0 ) 
{
// 
return false; 
}
else 
{
// 
return root->set( key, value ); 
}
}

// 
bool Tree::remove ( long long int key )
{
if ( root == 0 ) 
{
// 
return false; 
}
else if ( root->key == key && root->left == 0 && root->right == 0 ) 
{
// 
delete root; 
root = 0; 
return true; 
}
else 
{
// 
bool result = root->remove( key ); 
return result; 
}
}

// 
bool Tree::find ( long long int key, string & value ) 
{
if ( root == 0 ) 
{
// 
return false; 
}
else 
{
// 
return root->find( key, value ); 
}
}

// 
bool Tree::min ( long long int & key, string & value ) 
{
if ( root == 0 ) 
{
// 
return false; 
}
else 
{
// 
root->min( key, value ); 
return true; 
}
}

// 
bool Tree::max ( long long int & key, string & value )
{
if ( root == 0 ) 
{
// 
return false; 
}
else 
{
// 
root->max( key, value ); 
return true; 
}
}

// 
void Tree::print () 
{
if ( root == 0 ) 
{
// 
cout « "_\n"; 
}
else 
{
// 

// 
int max = 0; 
root->maxDepth( 0, max ); 

int goal = 0; 

for ( int i = 0; i <= max; i++ )
{
root->print( 0, goal ); 
cout « endl; 
goal ++; 
}
}
}

// 
bool readCommand ( string & command, long long int & k, string & v ) 
{
// 
string line; 
bool active = (bool) getline( cin, line ); 

stringstream ss( line ); 

// 
ss » command; 

// , 

if ( command == "add" || command == "set" ) 
{
ss » k; 
ss » v; 
}

if ( command == "delete" || command == "search" ) 
{
ss » k; 
}

return active; 
}

int main()
{
// 
Tree tree; 
// 
string command; 
// 
long long int key; 
// 
string value; 

while ( readCommand( command, key, value ) ) 
{
// 
if ( command == "add" ) 
{
bool result = tree.add( key, value ); 

if ( result == false ) 
{
cout « "error\n"; 
}
}
else if ( command == "set" ) 
{
bool result = tree.set( key, value ); 

if ( result == false ) 
{
cout « "error\n"; 
}
}
else if ( command == "delete" ) 
{
bool result = tree.remove( key ); 

if ( result == false ) 
{
cout « "error\n"; 
}
}
else if ( command == "search" ) 
{
bool result = tree.find( key, value ); 

if ( result == true ) 
{
cout « "1 " « value « endl; 
}
else 
{
cout « "0\n"; 
}
}
else if ( command == "min" ) 
{
bool result = tree.min( key, value ); 

if ( result == true ) 
{
cout « key « " " « value « endl; 
}
else
{
cout « "error\n"; 
}
}
else if ( command == "max" ) 
{
bool result = tree.max( key, value ); 

if ( result == true ) 
{
cout « key « " " « value « endl; 
}
else
{
cout « "error\n";
}
}
else if ( command == "print" ) 
{
tree.print(); 
}
else
{
// 
cout « "error\n"; 
}
}

return 0; 
}