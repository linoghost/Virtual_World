#include "Human.h"
#include <Windows.h>

Human::Human(int x, int y, World& world)
	:Animal(x, y, world)
{
	sign = 'Y';
	name = "Human";
	str = 5;
	ini = 4;
	speciesId = 11;
}
Human::Human(int str, int ini, int xPos, int yPos, int age, int oId, bool moved, World& world)
	:Animal(str, ini, xPos, yPos, age, oId, moved, world)
{
	sign = 'Y';
	name = "Human";
	speciesId = 11;
}
Animal* Human::MakeNewA(int x, int y) { return nullptr;}

int Human::GetCd() {
	return cooldown;
}
void Human::SetCd(int cooldown) {
	this->cooldown = cooldown;
}
int Human::GetP() {
	return powerLeft;
}
void Human::SetP(int powerLeft) {
	this->powerLeft = powerLeft;
}

void Human::SetAction(char action) {
	this->action = action;
}


void Human::TakeAction() {
	if (action == 'f' && !cooldown)
	{
		powerLeft = 5;
		cooldown = 10;
		cout << "Alzur's shield activated!" << endl;
		specialActivated = true;
		world.Print();
	}
	else {

		if (action == 'w')
			changeY--;
		else if (action == 's')
			changeY++;
		else if (action == 'a')
			changeX--;
		else if (action == 'd')
			changeX++;

		if (!(STAYS_IN_BOUNDS && (changeX || changeY)))
		{
			cout << " wrong input, try again!" << endl;
			changeX = 0;
			changeY = 0;
		}
		Organism* potentialCollision = world.LookForCollision(xPos + changeX, yPos + changeY);
		if (potentialCollision != nullptr) {
			Collision(*potentialCollision);
		}
		if (age != DEAD)
		{
			potentialCollision = world.LookForCollision(xPos + changeX, yPos + changeY);
			if (potentialCollision == nullptr)
			{
				cout << name << " moved from tile (" << xPos << ", " << yPos << ") to tile (" << xPos + changeX << ", " << yPos + changeY << ")" << endl;
				xPos += changeX;
				yPos += changeY;
			}
		}
		moved = true;
		if (age > 0) age++;
		if (cooldown)
			cooldown--;
		if (powerLeft)
			powerLeft--;
		changeX = 0;
		changeY = 0;
	}
	
	
	
		
}
void Human::Win(Organism& otherCreature)
{
	if (!specialActivated) {
		cout << " and " << name << " won! " << otherCreature.GetName() << " was eaten" << endl;
		world.RmOrganism(otherCreature.GetOId());
		otherCreature.SetAge(DEAD);
	}
}

bool Human::Defended(Organism& attackingCreature) {
	if (specialActivated) {
		attackingCreature.TakeAction();
		cout << " and " << name << " won! " << attackingCreature.GetName() << " was pushed back" << endl;
		return true;
	}
	else if (str>attackingCreature.GetS()){
		return true;
	}
	return false;
}

Human::~Human() {
}