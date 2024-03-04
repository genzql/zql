import { ReactNode } from "react";
// import { Label } from "@/components/ui/label";
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
// import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";

type HelpSheetProps = {
  children: ReactNode; // Accepts any valid React node
  value: string;
  setValue: (value: string) => void;
};

type QueryProps = {
  description: string;
  query: string;
};

const exampleQueryProps: QueryProps[] = [
  {
    description: "its giving",
    query: "its giving 1\nno cap",
  },
  {
    description: "yass",
    query: "its giving\n\tname,\n\tfave_color\nyass peeps\nno cap",
  },
  {
    description: "sheeeeeesh",
    query: "its giving\n\tsheeeeeesh\nyass peeps\nno cap",
  },
  {
    description: "say less",
    query: "its giving\n\tsheeeeeesh\nyass peeps\nsay less 3\nno cap",
  },
  {
    description: "tfw",
    query: "its giving\n\tsheeeeeesh\nyass peeps\ntfw name be 'vinesh'\nno cap",
  },
];

export function HelpSheet({ children, setValue }: HelpSheetProps) {
  const ExampleQueryCard: React.FC<QueryProps> = ({ description, query }) => {
    return (
      <div onClick={() => setValue(query)}>
        <Card className="flex flex-grow">
          <CardHeader>
            <CardTitle>{description}</CardTitle>
            <CardContent>{query}</CardContent>
          </CardHeader>
        </Card>
      </div>
    );
  };

  return (
    <Sheet>
      <SheetTrigger asChild>{children}</SheetTrigger>
      <SheetContent className="overflow-auto">
        <SheetHeader>
          <SheetTitle>Example zql queries</SheetTitle>
          <SheetDescription>Pre-filled zql to get you started</SheetDescription>
        </SheetHeader>
        <ScrollArea key="scroll-area">
          {exampleQueryProps.map((queryProp) => (
            <div key={queryProp.description} className="text-sm p-1 h-25">
              <SheetClose>
                <ExampleQueryCard {...queryProp} />
              </SheetClose>
            </div>
          ))}
        </ScrollArea>
        <SheetFooter></SheetFooter>
      </SheetContent>
    </Sheet>
  );
}
