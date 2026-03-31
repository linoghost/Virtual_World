#pragma once
#include "Animal.h"
class Human: public Animal
{
public:
	Human(int x, int y, World& world);
	Human(int str, int ini, int xPos, int yPos, int age, int oId, bool moved, World& world);

	int GetCd();
	int GetP();
	void SetCd(int cooldown);
	void SetP(int powerLeft);

	bool Defended(Organism& attackingCreature) override;
	void Win(Organism& otherCreature) override;

	void TakeAction() override;
	Animal* MakeNewA(int x, int y) override;
	void SetAction(char action);
	~Human() override;
	
private:
	int cooldown = 0, powerLeft = 0;
	char action;
	int changeX = 0, changeY = 0;
	bool specialActivated = false;
};
