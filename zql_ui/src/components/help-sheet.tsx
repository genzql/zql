import { ReactNode } from "react";
import {
  Sheet,
  SheetClose,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { ScrollArea } from "@radix-ui/react-scroll-area";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { exampleQueries } from "./exampleQueries";
import { exampleQuery } from "./exampleQueries";

type HelpSheetProps = {
  children: ReactNode; // Accepts any valid React node
  value: string;
  setValue: (value: string) => void;
  open: boolean;
  onOpenChange: (value: boolean) => void;
};

export function HelpSheet({
  children,
  setValue,
  open,
  onOpenChange,
}: HelpSheetProps) {
  const ExampleQueryCard: React.FC<exampleQuery> = (exampleQuery) => {
    return (
      <div onClick={() => setValue(exampleQuery.query)}>
        <Card className="flex flex-grow">
          <CardHeader className="w-full">
            <CardTitle>{exampleQuery.title}</CardTitle>
            <CardContent>{exampleQuery.query}</CardContent>
          </CardHeader>
        </Card>
      </div>
    );
  };

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetTrigger asChild>{children}</SheetTrigger>
      <SheetContent className="overflow-auto">
        <SheetHeader>
          <SheetTitle>inspo zql queries</SheetTitle>
          <SheetDescription>
            pre-filled zql that you know is bussin'
          </SheetDescription>
        </SheetHeader>
        <ScrollArea key="scroll-area">
          {exampleQueries.map((exampleQuery) => (
            <div key={exampleQuery.title} className="text-sm p-1 h-25">
              <SheetClose className="w-full">
                <ExampleQueryCard {...exampleQuery} />
              </SheetClose>
            </div>
          ))}
        </ScrollArea>
        <SheetFooter></SheetFooter>
      </SheetContent>
    </Sheet>
  );
}
