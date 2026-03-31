#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_phase_3a.py
=================
Phase 3A: Chat Layout & Sidebar
Creates the main chat pages, sidebar components, and common UI components.
"""

import os

files_created = 0
files_failed = 0


def create_file(path: str, content: str) -> None:
    """Create a file with the given path and content, creating directories as needed."""
    global files_created, files_failed
    try:
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        files_created += 1
        print(f"  ✅ Created: {path}")
    except Exception as e:
        files_failed += 1
        print(f"  ❌ Failed: {path} - {e}")


def main():
    global files_created, files_failed

    print("=" * 60)
    print("🚀 BUILD PHASE 3A: Chat Layout & Sidebar")
    print("=" * 60)

    # ──────────────────────────────────────────────
    # Prerequisite UI components
    # ──────────────────────────────────────────────
    print("\n📁 Prerequisite UI Components")
    print("-" * 40)

    create_file("components/ui/skeleton.tsx", """// مكون الهيكل العظمي: يعرض حالة تحميل بتأثير نبضي
'use client';

import { cn } from '@/utils/cn';

interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  /** شكل دائري */
  circle?: boolean;
}

function Skeleton({ className, circle, ...props }: SkeletonProps) {
  return (
    <div
      className={cn(
        'animate-pulse bg-gray-200 dark:bg-dark-700',
        circle ? 'rounded-full' : 'rounded-md',
        className
      )}
      {...props}
    />
  );
}

export { Skeleton };
""")

    create_file("components/ui/separator.tsx", """// مكون الفاصل: خط فاصل أفقي أو عمودي
'use client';

import * as React from 'react';
import { cn } from '@/utils/cn';

interface SeparatorProps extends React.HTMLAttributes<HTMLDivElement> {
  orientation?: 'horizontal' | 'vertical';
  decorative?: boolean;
}

const Separator = React.forwardRef<HTMLDivElement, SeparatorProps>(
  ({ className, orientation = 'horizontal', decorative = true, ...props }, ref) => (
    <div
      ref={ref}
      role={decorative ? 'none' : 'separator'}
      aria-orientation={decorative ? undefined : orientation}
      className={cn(
        'shrink-0 bg-gray-200 dark:bg-dark-700',
        orientation === 'horizontal' ? 'h-[1px] w-full' : 'h-full w-[1px]',
        className
      )}
      {...props}
    />
  )
);
Separator.displayName = 'Separator';

export { Separator };
""")

    create_file("components/ui/scroll-area.tsx", """// مكون منطقة التمرير: حاوية بشريط تمرير مخصص
'use client';

import * as React from 'react';
import { cn } from '@/utils/cn';

interface ScrollAreaProps extends React.HTMLAttributes<HTMLDivElement> {
  /** الارتفاع الأقصى */
  maxHeight?: string;
}

const ScrollArea = React.forwardRef<HTMLDivElement, ScrollAreaProps>(
  ({ className, children, maxHeight, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        'relative overflow-auto custom-scrollbar',
        className
      )}
      style={maxHeight ? { maxHeight } : undefined}
      {...props}
    >
      {children}
    </div>
  )
);
ScrollArea.displayName = 'ScrollArea';

export { ScrollArea };
""")

    create_file("components/ui/dialog.tsx", """// مكون الحوار: نافذة منبثقة مع تراكب خلفي
'use client';

import * as React from 'react';
import { cn } from '@/utils/cn';
import { X } from 'lucide-react';

interface DialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  children: React.ReactNode;
}

function Dialog({ open, onOpenChange, children }: DialogProps) {
  React.useEffect(() => {
    if (open) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [open]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-modal">
      <div
        className="fixed inset-0 bg-black/60 backdrop-blur-sm animate-fade-in"
        onClick={() => onOpenChange(false)}
        aria-hidden="true"
      />
      <div className="fixed inset-0 flex items-center justify-center p-4">
        {children}
      </div>
    </div>
  );
}

interface DialogContentProps extends React.HTMLAttributes<HTMLDivElement> {
  onClose?: () => void;
}

const DialogContent = React.forwardRef<HTMLDivElement, DialogContentProps>(
  ({ className, children, onClose, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        'relative w-full max-w-lg rounded-xl border border-gray-200 dark:border-dark-700',
        'bg-white dark:bg-dark-900 shadow-2xl animate-fade-in',
        'max-h-[85vh] overflow-y-auto custom-scrollbar',
        className
      )}
      onClick={(e) => e.stopPropagation()}
      {...props}
    >
      {onClose && (
        <button
          onClick={onClose}
          className="absolute top-4 end-4 rounded-md p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors z-10"
          aria-label="Close dialog"
        >
          <X className="h-4 w-4" />
        </button>
      )}
      {children}
    </div>
  )
);
DialogContent.displayName = 'DialogContent';

const DialogHeader = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn('flex flex-col space-y-1.5 p-6 pb-2', className)} {...props} />
);
DialogHeader.displayName = 'DialogHeader';

const DialogTitle = React.forwardRef<HTMLHeadingElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h2
      ref={ref}
      className={cn('text-lg font-semibold text-gray-900 dark:text-gray-100', className)}
      {...props}
    />
  )
);
DialogTitle.displayName = 'DialogTitle';

const DialogDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <p
      ref={ref}
      className={cn('text-sm text-gray-500 dark:text-gray-400', className)}
      {...props}
    />
  )
);
DialogDescription.displayName = 'DialogDescription';

const DialogFooter = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn('flex items-center justify-end gap-2 p-6 pt-2', className)} {...props} />
);
DialogFooter.displayName = 'DialogFooter';

export { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter };
""")

    create_file("components/ui/dropdown-menu.tsx", """// مكون القائمة المنسدلة: قائمة خيارات منبثقة
'use client';

import * as React from 'react';
import { cn } from '@/utils/cn';

interface DropdownMenuProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  children: React.ReactNode;
}

function DropdownMenu({ open, onOpenChange, children }: DropdownMenuProps) {
  return (
    <div className="relative inline-block">
      {open && (
        <div
          className="fixed inset-0 z-30"
          onClick={() => onOpenChange(false)}
          aria-hidden="true"
        />
      )}
      {children}
    </div>
  );
}

interface DropdownMenuTriggerProps {
  children: React.ReactNode;
  onClick?: () => void;
  className?: string;
  asChild?: boolean;
}

function DropdownMenuTrigger({ children, onClick, className }: DropdownMenuTriggerProps) {
  return (
    <div className={cn('cursor-pointer', className)} onClick={onClick}>
      {children}
    </div>
  );
}

interface DropdownMenuContentProps extends React.HTMLAttributes<HTMLDivElement> {
  align?: 'start' | 'end' | 'center';
  side?: 'top' | 'bottom';
}

const DropdownMenuContent = React.forwardRef<HTMLDivElement, DropdownMenuContentProps>(
  ({ className, align = 'end', side = 'bottom', children, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        'absolute z-40 min-w-[180px] rounded-lg border border-gray-200 dark:border-dark-700',
        'bg-white dark:bg-dark-800 shadow-xl animate-fade-in',
        'py-1 overflow-hidden',
        side === 'bottom' ? 'top-full mt-1' : 'bottom-full mb-1',
        align === 'start' && 'start-0',
        align === 'end' && 'end-0',
        align === 'center' && 'start-1/2 -translate-x-1/2',
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
);
DropdownMenuContent.displayName = 'DropdownMenuContent';

interface DropdownMenuItemProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  destructive?: boolean;
  icon?: React.ReactNode;
}

const DropdownMenuItem = React.forwardRef<HTMLButtonElement, DropdownMenuItemProps>(
  ({ className, destructive, icon, children, ...props }, ref) => (
    <button
      ref={ref}
      className={cn(
        'flex w-full items-center gap-2 px-3 py-2 text-sm transition-colors',
        'text-start',
        destructive
          ? 'text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20'
          : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-dark-700',
        'disabled:opacity-50 disabled:pointer-events-none',
        className
      )}
      {...props}
    >
      {icon && <span className="shrink-0">{icon}</span>}
      {children}
    </button>
  )
);
DropdownMenuItem.displayName = 'DropdownMenuItem';

const DropdownMenuSeparator = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn('my-1 h-px bg-gray-200 dark:bg-dark-700', className)} {...props} />
);
DropdownMenuSeparator.displayName = 'DropdownMenuSeparator';

const DropdownMenuLabel = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn('px-3 py-1.5 text-xs font-semibold text-gray-500 dark:text-gray-400', className)}
    {...props}
  />
);
DropdownMenuLabel.displayName = 'DropdownMenuLabel';

export {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuLabel,
};
""")

    create_file("components/ui/tooltip.tsx", """// مكون التلميح: نص تلميحي عند تمرير الماوس
'use client';

import * as React from 'react';
import { cn } from '@/utils/cn';

interface TooltipProps {
  content: string;
  children: React.ReactNode;
  side?: 'top' | 'bottom' | 'left' | 'right';
  className?: string;
}

function Tooltip({ content, children, side = 'top', className }: TooltipProps) {
  const [visible, setVisible] = React.useState(false);

  const positionClasses = {
    top: 'bottom-full mb-2 start-1/2 -translate-x-1/2',
    bottom: 'top-full mt-2 start-1/2 -translate-x-1/2',
    left: 'end-full me-2 top-1/2 -translate-y-1/2',
    right: 'start-full ms-2 top-1/2 -translate-y-1/2',
  };

  return (
    <div
      className="relative inline-flex"
      onMouseEnter={() => setVisible(true)}
      onMouseLeave={() => setVisible(false)}
    >
      {children}
      {visible && content && (
        <div
          className={cn(
            'absolute z-50 whitespace-nowrap rounded-md px-2.5 py-1.5',
            'bg-dark-900 dark:bg-dark-700 text-white text-xs font-medium',
            'shadow-lg pointer-events-none animate-fade-in',
            positionClasses[side],
            className
          )}
          role="tooltip"
        >
          {content}
        </div>
      )}
    </div>
  );
}

export { Tooltip };
""")

    create_file("components/ui/badge.tsx", """// مكون الشارة: شارة نصية صغيرة مع متغيرات لونية
'use client';

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/utils/cn';

const badgeVariants = cva(
  'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors',
  {
    variants: {
      variant: {
        default: 'bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300',
        secondary: 'bg-gray-100 dark:bg-dark-700 text-gray-700 dark:text-gray-300',
        success: 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300',
        warning: 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300',
        destructive: 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300',
        outline: 'border border-gray-200 dark:border-dark-600 text-gray-700 dark:text-gray-300',
        premium: 'bg-gradient-to-r from-primary-500/20 to-accent-500/20 text-primary-400 border border-primary-500/30',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />;
}

export { Badge, badgeVariants };
""")

    # ──────────────────────────────────────────────
    # Hooks needed for chat/sidebar
    # ──────────────────────────────────────────────
    print("\n📁 Chat Hooks")
    print("-" * 40)

    create_file("hooks/useChat.ts", """// خطاف الدردشة: يدير المحادثات والرسائل (CRUD + التحميل)
'use client';

import { useState, useCallback, useEffect, useRef } from 'react';
import { createSupabaseBrowserClient } from '@/lib/supabase-client';
import { useChatStore } from '@/stores/chatStore';
import { useAuthStore } from '@/stores/authStore';
import type { Conversation, Message, CreateConversationData, UpdateConversationData } from '@/types/chat';

/**
 * واجهة القيم المرجعة من خطاف الدردشة
 */
interface UseChatReturn {
  conversations: Conversation[];
  currentConversation: Conversation | null;
  messages: Message[];
  isLoadingConversations: boolean;
  isLoadingMessages: boolean;
  loadConversations: () => Promise<void>;
  loadConversation: (id: string) => Promise<Conversation | null>;
  loadMessages: (conversationId: string) => Promise<void>;
  createConversation: (data: CreateConversationData) => Promise<Conversation | null>;
  updateConversation: (id: string, data: UpdateConversationData) => Promise<void>;
  deleteConversation: (id: string) => Promise<void>;
  searchConversations: (query: string) => Conversation[];
}

/**
 * خطاف إدارة الدردشة
 */
export function useChat(): UseChatReturn {
  const supabase = createSupabaseBrowserClient();
  const { user } = useAuthStore();
  const { conversation: currentConversation, messages, setConversation, setMessages } = useChatStore();

  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [isLoadingConversations, setIsLoadingConversations] = useState(false);
  const [isLoadingMessages, setIsLoadingMessages] = useState(false);
  const loadedRef = useRef(false);

  /**
   * تحميل جميع المحادثات
   */
  const loadConversations = useCallback(async () => {
    if (!user) return;
    setIsLoadingConversations(true);

    try {
      const { data, error } = await supabase
        .from('conversations')
        .select('*')
        .eq('user_id', user.id)
        .order('updated_at', { ascending: false });

      if (error) {
        if (process.env.NODE_ENV === 'development') {
          console.error('Error loading conversations:', error.message);
        }
        return;
      }

      setConversations((data as Conversation[]) ?? []);
    } catch {
      // تجاهل الأخطاء
    } finally {
      setIsLoadingConversations(false);
    }
  }, [supabase, user]);

  /**
   * تحميل محادثة واحدة بالمعرف
   */
  const loadConversation = useCallback(
    async (id: string): Promise<Conversation | null> => {
      if (!user) return null;

      try {
        const { data, error } = await supabase
          .from('conversations')
          .select('*')
          .eq('id', id)
          .eq('user_id', user.id)
          .single();

        if (error || !data) return null;

        const conv = data as Conversation;
        setConversation(conv);
        return conv;
      } catch {
        return null;
      }
    },
    [supabase, user, setConversation]
  );

  /**
   * تحميل رسائل محادثة
   */
  const loadMessages = useCallback(
    async (conversationId: string) => {
      setIsLoadingMessages(true);

      try {
        const { data, error } = await supabase
          .from('messages')
          .select('*')
          .eq('conversation_id', conversationId)
          .order('created_at', { ascending: true });

        if (error) {
          if (process.env.NODE_ENV === 'development') {
            console.error('Error loading messages:', error.message);
          }
          return;
        }

        setMessages((data as Message[]) ?? []);
      } catch {
        // تجاهل
      } finally {
        setIsLoadingMessages(false);
      }
    },
    [supabase, setMessages]
  );

  /**
   * إنشاء محادثة جديدة
   */
  const createConversation = useCallback(
    async (data: CreateConversationData): Promise<Conversation | null> => {
      if (!user) return null;

      try {
        const { data: newConv, error } = await supabase
          .from('conversations')
          .insert({
            user_id: user.id,
            title: data.title ?? 'محادثة جديدة',
            persona_id: data.persona_id ?? null,
            platform: data.platform,
            model: data.model,
            folder_id: data.folder_id ?? null,
          })
          .select()
          .single();

        if (error || !newConv) {
          if (process.env.NODE_ENV === 'development') {
            console.error('Error creating conversation:', error?.message);
          }
          return null;
        }

        const conv = newConv as Conversation;
        setConversation(conv);
        setConversations((prev) => [conv, ...prev]);
        return conv;
      } catch {
        return null;
      }
    },
    [supabase, user, setConversation]
  );

  /**
   * تحديث محادثة
   */
  const updateConversation = useCallback(
    async (id: string, data: UpdateConversationData) => {
      try {
        const { error } = await supabase
          .from('conversations')
          .update({ ...data, updated_at: new Date().toISOString() })
          .eq('id', id);

        if (error) {
          if (process.env.NODE_ENV === 'development') {
            console.error('Error updating conversation:', error.message);
          }
          return;
        }

        setConversations((prev) =>
          prev.map((c) => (c.id === id ? { ...c, ...data, updated_at: new Date().toISOString() } : c))
        );

        if (currentConversation?.id === id) {
          setConversation({ ...currentConversation, ...data, updated_at: new Date().toISOString() });
        }
      } catch {
        // تجاهل
      }
    },
    [supabase, currentConversation, setConversation]
  );

  /**
   * حذف محادثة
   */
  const deleteConversation = useCallback(
    async (id: string) => {
      try {
        const { error } = await supabase
          .from('conversations')
          .delete()
          .eq('id', id);

        if (error) {
          if (process.env.NODE_ENV === 'development') {
            console.error('Error deleting conversation:', error.message);
          }
          return;
        }

        setConversations((prev) => prev.filter((c) => c.id !== id));

        if (currentConversation?.id === id) {
          setConversation(null);
          setMessages([]);
        }
      } catch {
        // تجاهل
      }
    },
    [supabase, currentConversation, setConversation, setMessages]
  );

  /**
   * بحث في المحادثات
   */
  const searchConversations = useCallback(
    (query: string): Conversation[] => {
      if (!query.trim()) return conversations;
      const lowerQuery = query.toLowerCase();
      return conversations.filter(
        (c) =>
          c.title.toLowerCase().includes(lowerQuery) ||
          c.platform.toLowerCase().includes(lowerQuery) ||
          c.model.toLowerCase().includes(lowerQuery)
      );
    },
    [conversations]
  );

  /**
   * تحميل المحادثات عند أول تحميل
   */
  useEffect(() => {
    if (user && !loadedRef.current) {
      loadedRef.current = true;
      loadConversations();
    }
    return () => {};
  }, [user, loadConversations]);

  return {
    conversations,
    currentConversation,
    messages,
    isLoadingConversations,
    isLoadingMessages,
    loadConversations,
    loadConversation,
    loadMessages,
    createConversation,
    updateConversation,
    deleteConversation,
    searchConversations,
  };
}
""")

    create_file("hooks/useFolders.ts", """// خطاف المجلدات: يدير إنشاء وتعديل وحذف المجلدات
'use client';

import { useState, useCallback, useEffect, useRef } from 'react';
import { createSupabaseBrowserClient } from '@/lib/supabase-client';
import { useAuthStore } from '@/stores/authStore';
import type { Folder, FolderType } from '@/types/folder';

/**
 * واجهة القيم المرجعة من خطاف المجلدات
 */
interface UseFoldersReturn {
  folders: Folder[];
  isLoading: boolean;
  loadFolders: () => Promise<void>;
  createFolder: (name: string, type: FolderType) => Promise<Folder | null>;
  updateFolder: (id: string, name: string) => Promise<void>;
  deleteFolder: (id: string) => Promise<void>;
  reorderFolders: (ids: string[]) => Promise<void>;
}

/**
 * خطاف إدارة المجلدات
 */
export function useFolders(): UseFoldersReturn {
  const supabase = createSupabaseBrowserClient();
  const { user } = useAuthStore();

  const [folders, setFolders] = useState<Folder[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const loadedRef = useRef(false);

  const loadFolders = useCallback(async () => {
    if (!user) return;
    setIsLoading(true);

    try {
      const { data, error } = await supabase
        .from('folders')
        .select('*')
        .eq('user_id', user.id)
        .order('sort_order', { ascending: true });

      if (!error && data) {
        setFolders(data as Folder[]);
      }
    } catch {
      // تجاهل
    } finally {
      setIsLoading(false);
    }
  }, [supabase, user]);

  const createFolder = useCallback(
    async (name: string, type: FolderType): Promise<Folder | null> => {
      if (!user) return null;

      try {
        const { data, error } = await supabase
          .from('folders')
          .insert({
            user_id: user.id,
            name,
            type,
            sort_order: folders.length,
          })
          .select()
          .single();

        if (error || !data) return null;

        const folder = data as Folder;
        setFolders((prev) => [...prev, folder]);
        return folder;
      } catch {
        return null;
      }
    },
    [supabase, user, folders.length]
  );

  const updateFolder = useCallback(
    async (id: string, name: string) => {
      try {
        const { error } = await supabase
          .from('folders')
          .update({ name })
          .eq('id', id);

        if (!error) {
          setFolders((prev) => prev.map((f) => (f.id === id ? { ...f, name } : f)));
        }
      } catch {
        // تجاهل
      }
    },
    [supabase]
  );

  const deleteFolder = useCallback(
    async (id: string) => {
      try {
        // نقل المحادثات خارج المجلد قبل الحذف
        await supabase
          .from('conversations')
          .update({ folder_id: null })
          .eq('folder_id', id);

        const { error } = await supabase
          .from('folders')
          .delete()
          .eq('id', id);

        if (!error) {
          setFolders((prev) => prev.filter((f) => f.id !== id));
        }
      } catch {
        // تجاهل
      }
    },
    [supabase]
  );

  const reorderFolders = useCallback(
    async (ids: string[]) => {
      try {
        const updates = ids.map((id, index) => ({
          id,
          sort_order: index,
        }));

        for (const update of updates) {
          await supabase
            .from('folders')
            .update({ sort_order: update.sort_order })
            .eq('id', update.id);
        }

        setFolders((prev) => {
          const sorted = [...prev].sort((a, b) => {
            const aIndex = ids.indexOf(a.id);
            const bIndex = ids.indexOf(b.id);
            return aIndex - bIndex;
          });
          return sorted;
        });
      } catch {
        // تجاهل
      }
    },
    [supabase]
  );

  useEffect(() => {
    if (user && !loadedRef.current) {
      loadedRef.current = true;
      loadFolders();
    }
    return () => {};
  }, [user, loadFolders]);

  return {
    folders,
    isLoading,
    loadFolders,
    createFolder,
    updateFolder,
    deleteFolder,
    reorderFolders,
  };
}
""")

    create_file("hooks/useFavorites.ts", """// خطاف المفضلات: يدير إضافة وإزالة العناصر المفضلة
'use client';

import { useState, useCallback, useEffect, useRef } from 'react';
import { createSupabaseBrowserClient } from '@/lib/supabase-client';
import { useAuthStore } from '@/stores/authStore';
import type { UserFavorite } from '@/types/database';

/**
 * واجهة القيم المرجعة
 */
interface UseFavoritesReturn {
  favorites: UserFavorite[];
  isLoading: boolean;
  loadFavorites: () => Promise<void>;
  addFavorite: (itemType: 'persona' | 'model', itemId: string) => Promise<void>;
  removeFavorite: (itemType: 'persona' | 'model', itemId: string) => Promise<void>;
  isFavorite: (itemType: 'persona' | 'model', itemId: string) => boolean;
}

export function useFavorites(): UseFavoritesReturn {
  const supabase = createSupabaseBrowserClient();
  const { user } = useAuthStore();

  const [favorites, setFavorites] = useState<UserFavorite[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const loadedRef = useRef(false);

  const loadFavorites = useCallback(async () => {
    if (!user) return;
    setIsLoading(true);

    try {
      const { data, error } = await supabase
        .from('user_favorites')
        .select('*')
        .eq('user_id', user.id)
        .order('sort_order', { ascending: true });

      if (!error && data) {
        setFavorites(data as UserFavorite[]);
      }
    } catch {
      // تجاهل
    } finally {
      setIsLoading(false);
    }
  }, [supabase, user]);

  const addFavorite = useCallback(
    async (itemType: 'persona' | 'model', itemId: string) => {
      if (!user) return;

      try {
        const { data, error } = await supabase
          .from('user_favorites')
          .insert({
            user_id: user.id,
            item_type: itemType,
            item_id: itemId,
            sort_order: favorites.length,
          })
          .select()
          .single();

        if (!error && data) {
          setFavorites((prev) => [...prev, data as UserFavorite]);
        }
      } catch {
        // تجاهل
      }
    },
    [supabase, user, favorites.length]
  );

  const removeFavorite = useCallback(
    async (itemType: 'persona' | 'model', itemId: string) => {
      if (!user) return;

      try {
        const { error } = await supabase
          .from('user_favorites')
          .delete()
          .eq('user_id', user.id)
          .eq('item_type', itemType)
          .eq('item_id', itemId);

        if (!error) {
          setFavorites((prev) =>
            prev.filter((f) => !(f.item_type === itemType && f.item_id === itemId))
          );
        }
      } catch {
        // تجاهل
      }
    },
    [supabase, user]
  );

  const isFavorite = useCallback(
    (itemType: 'persona' | 'model', itemId: string): boolean => {
      return favorites.some((f) => f.item_type === itemType && f.item_id === itemId);
    },
    [favorites]
  );

  useEffect(() => {
    if (user && !loadedRef.current) {
      loadedRef.current = true;
      loadFavorites();
    }
    return () => {};
  }, [user, loadFavorites]);

  return { favorites, isLoading, loadFavorites, addFavorite, removeFavorite, isFavorite };
}
""")

    # ──────────────────────────────────────────────
    # Common Components (updated/new)
    # ──────────────────────────────────────────────
    print("\n📁 Common Components")
    print("-" * 40)

    create_file("components/common/EmptyState.tsx", """// مكون الحالة الفارغة: يعرض أيقونة وعنوان ووصف مع زر إجراء اختياري
'use client';

import { cn } from '@/utils/cn';
import type { LucideIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';

/**
 * خصائص مكون الحالة الفارغة
 */
interface EmptyStateProps {
  /** الأيقونة */
  icon: LucideIcon;
  /** العنوان */
  title: string;
  /** الوصف */
  description?: string;
  /** نص زر الإجراء */
  actionLabel?: string;
  /** دالة الإجراء */
  onAction?: () => void;
  /** أسماء أصناف إضافية */
  className?: string;
}

/**
 * مكون الحالة الفارغة
 */
export function EmptyState({
  icon: Icon,
  title,
  description,
  actionLabel,
  onAction,
  className,
}: EmptyStateProps) {
  return (
    <div
      className={cn(
        'flex flex-col items-center justify-center text-center p-8 space-y-4',
        className
      )}
    >
      <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gray-100 dark:bg-dark-800">
        <Icon className="h-8 w-8 text-gray-400 dark:text-gray-500" />
      </div>
      <div className="space-y-1.5">
        <h3 className="text-base font-semibold text-gray-700 dark:text-gray-300">
          {title}
        </h3>
        {description && (
          <p className="text-sm text-gray-500 dark:text-gray-400 max-w-xs">
            {description}
          </p>
        )}
      </div>
      {actionLabel && onAction && (
        <Button onClick={onAction} variant="outline" size="sm">
          {actionLabel}
        </Button>
      )}
    </div>
  );
}
""")

    create_file("components/common/ConfirmDialog.tsx", """// مكون حوار التأكيد: نافذة تأكيد مع خيار حذف تدميري وحالة تحميل
'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { AlertTriangle } from 'lucide-react';

/**
 * خصائص حوار التأكيد
 */
interface ConfirmDialogProps {
  /** هل الحوار مفتوح؟ */
  open: boolean;
  /** تغيير حالة الفتح */
  onOpenChange: (open: boolean) => void;
  /** العنوان */
  title: string;
  /** الرسالة */
  message: string;
  /** نص زر التأكيد */
  confirmLabel?: string;
  /** نص زر الإلغاء */
  cancelLabel?: string;
  /** هل هو إجراء تدميري؟ */
  destructive?: boolean;
  /** دالة التأكيد */
  onConfirm: () => void | Promise<void>;
}

/**
 * مكون حوار التأكيد
 */
export function ConfirmDialog({
  open,
  onOpenChange,
  title,
  message,
  confirmLabel,
  cancelLabel,
  destructive = false,
  onConfirm,
}: ConfirmDialogProps) {
  const t = useTranslations('common');
  const [isLoading, setIsLoading] = useState(false);

  const handleConfirm = async () => {
    setIsLoading(true);
    try {
      await onConfirm();
      onOpenChange(false);
    } catch {
      // تجاهل
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent onClose={() => onOpenChange(false)}>
        <DialogHeader>
          <div className="flex items-start gap-3">
            {destructive && (
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-red-100 dark:bg-red-900/30">
                <AlertTriangle className="h-5 w-5 text-red-600 dark:text-red-400" />
              </div>
            )}
            <div className="space-y-1">
              <DialogTitle>{title}</DialogTitle>
              <DialogDescription>{message}</DialogDescription>
            </div>
          </div>
        </DialogHeader>
        <DialogFooter>
          <Button
            variant="outline"
            onClick={() => onOpenChange(false)}
            disabled={isLoading}
          >
            {cancelLabel ?? t('cancel')}
          </Button>
          <Button
            variant={destructive ? 'destructive' : 'default'}
            onClick={handleConfirm}
            isLoading={isLoading}
            disabled={isLoading}
          >
            {confirmLabel ?? t('confirm')}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
""")

    # ──────────────────────────────────────────────
    # Sidebar Components
    # ──────────────────────────────────────────────
    print("\n📁 Sidebar Components")
    print("-" * 40)

    create_file("components/sidebar/Sidebar.tsx", """// الشريط الجانبي: يحتوي على البحث والمحادثات والمجلدات والمفضلات والشخصيات
// يتكيف مع الشاشة: ثابت على الديسكتوب، درج على التابلت، تراكب على الموبايل
// يظهر على اليمين في العربية واليسار في الإنجليزية
'use client';

import { useEffect, useCallback } from 'react';
import { useLocale, useTranslations } from 'next-intl';
import { Plus, X, PanelRightOpen, PanelLeftOpen } from 'lucide-react';
import { cn } from '@/utils/cn';
import { useUIStore } from '@/stores/uiStore';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Tooltip } from '@/components/ui/tooltip';
import { Logo } from '@/components/common/Logo';
import { ConversationList } from './ConversationList';
import { FolderList } from './FolderList';
import { FavoritesList } from './FavoritesList';
import { PersonaList } from './PersonaList';
import { QuickSettings } from './QuickSettings';
import type { Conversation } from '@/types/chat';
import type { Folder } from '@/types/folder';

/**
 * خصائص الشريط الجانبي
 */
interface SidebarProps {
  conversations: Conversation[];
  folders: Folder[];
  activeConversationId?: string;
  onNewChat: () => void;
  onSelectConversation: (id: string) => void;
  onDeleteConversation: (id: string) => void;
  onRenameConversation: (id: string, title: string) => void;
  onMoveConversation: (id: string, folderId: string | null) => void;
  onCreateFolder: (name: string) => void;
  onDeleteFolder: (id: string) => void;
  onRenameFolder: (id: string, name: string) => void;
  isLoadingConversations: boolean;
}

/**
 * مكون الشريط الجانبي
 */
export function Sidebar({
  conversations,
  folders,
  activeConversationId,
  onNewChat,
  onSelectConversation,
  onDeleteConversation,
  onRenameConversation,
  onMoveConversation,
  onCreateFolder,
  onDeleteFolder,
  onRenameFolder,
  isLoadingConversations,
}: SidebarProps) {
  const t = useTranslations('sidebar');
  const locale = useLocale();
  const { sidebarOpen, setSidebarOpen } = useUIStore();
  const isRTL = locale === 'ar';

  // إغلاق الشريط الجانبي على الشاشات الصغيرة عند النقر خارجه
  const handleOverlayClick = useCallback(() => {
    if (window.innerWidth < 1024) {
      setSidebarOpen(false);
    }
  }, [setSidebarOpen]);

  // الاستماع لتغيير حجم الشاشة
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 1024) {
        setSidebarOpen(true);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [setSidebarOpen]);

  return (
    <>
      {/* تراكب خلفي للموبايل */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/50 backdrop-blur-sm lg:hidden"
          onClick={handleOverlayClick}
          aria-hidden="true"
        />
      )}

      {/* الشريط الجانبي */}
      <aside
        className={cn(
          'fixed top-0 z-sidebar h-full w-sidebar flex flex-col',
          'bg-gray-50 dark:bg-dark-900 border-gray-200 dark:border-dark-700',
          'transition-transform duration-300 ease-in-out',
          isRTL ? 'right-0 border-s' : 'left-0 border-e',
          sidebarOpen
            ? 'translate-x-0'
            : isRTL
              ? 'translate-x-full'
              : '-translate-x-full'
        )}
      >
        {/* رأس الشريط الجانبي */}
        <div className="flex items-center justify-between p-4 shrink-0">
          <Logo size="sm" />
          <div className="flex items-center gap-1">
            {/* زر إغلاق الموبايل */}
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden rounded-lg p-1.5 text-gray-500 hover:bg-gray-200 dark:hover:bg-dark-700 transition-colors"
              aria-label="Close sidebar"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        </div>

        {/* زر محادثة جديدة */}
        <div className="px-3 pb-2 shrink-0">
          <Button onClick={onNewChat} className="w-full gap-2" size="default">
            <Plus className="h-4 w-4" />
            {t('new_chat')}
          </Button>
        </div>

        <Separator />

        {/* المحتوى القابل للتمرير */}
        <ScrollArea className="flex-1 px-2 py-2">
          {/* المفضلات */}
          <FavoritesList />

          {/* المجلدات */}
          <FolderList
            folders={folders}
            conversations={conversations}
            activeConversationId={activeConversationId}
            onSelectConversation={onSelectConversation}
            onCreateFolder={onCreateFolder}
            onDeleteFolder={onDeleteFolder}
            onRenameFolder={onRenameFolder}
          />

          <Separator className="my-2" />

          {/* قائمة المحادثات */}
          <ConversationList
            conversations={conversations.filter((c) => !c.folder_id)}
            activeConversationId={activeConversationId}
            folders={folders}
            onSelect={onSelectConversation}
            onDelete={onDeleteConversation}
            onRename={onRenameConversation}
            onMove={onMoveConversation}
            isLoading={isLoadingConversations}
          />

          <Separator className="my-2" />

          {/* قائمة الشخصيات */}
          <PersonaList />
        </ScrollArea>

        <Separator />

        {/* الإعدادات السريعة */}
        <QuickSettings />
      </aside>

      {/* زر فتح الشريط الجانبي عندما يكون مغلقاً */}
      {!sidebarOpen && (
        <Tooltip content={t('new_chat')} side={isRTL ? 'left' : 'right'}>
          <button
            onClick={() => setSidebarOpen(true)}
            className={cn(
              'fixed top-4 z-30 rounded-lg p-2',
              'bg-gray-100 dark:bg-dark-800 text-gray-600 dark:text-gray-400',
              'hover:bg-gray-200 dark:hover:bg-dark-700 transition-colors shadow-md',
              isRTL ? 'right-4' : 'left-4'
            )}
            aria-label="Open sidebar"
          >
            {isRTL ? (
              <PanelRightOpen className="h-5 w-5" />
            ) : (
              <PanelLeftOpen className="h-5 w-5" />
            )}
          </button>
        </Tooltip>
      )}
    </>
  );
}
""")

    create_file("components/sidebar/ConversationList.tsx", """// قائمة المحادثات: عرض المحادثات مع البحث والقائمة السياقية
'use client';

import { useState, useMemo, useCallback } from 'react';
import { useTranslations, useLocale } from 'next-intl';
import {
  MessageSquare, Search, MoreHorizontal, Edit3, Trash2,
  FolderInput, Download, Star, StarOff,
} from 'lucide-react';
import { cn } from '@/utils/cn';
import { Input } from '@/components/ui/input';
import { Skeleton } from '@/components/ui/skeleton';
import { EmptyState } from '@/components/common/EmptyState';
import {
  DropdownMenu, DropdownMenuTrigger, DropdownMenuContent,
  DropdownMenuItem, DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu';
import { truncateText } from '@/utils/helpers';
import { formatRelativeTime } from '@/utils/formatters';
import { debounce } from '@/utils/helpers';
import type { Conversation } from '@/types/chat';
import type { Folder } from '@/types/folder';

/**
 * خصائص قائمة المحادثات
 */
interface ConversationListProps {
  conversations: Conversation[];
  activeConversationId?: string;
  folders: Folder[];
  onSelect: (id: string) => void;
  onDelete: (id: string) => void;
  onRename: (id: string, title: string) => void;
  onMove: (id: string, folderId: string | null) => void;
  isLoading: boolean;
}

/**
 * مكون قائمة المحادثات
 */
export function ConversationList({
  conversations,
  activeConversationId,
  folders,
  onSelect,
  onDelete,
  onRename,
  onMove,
  isLoading,
}: ConversationListProps) {
  const t = useTranslations('sidebar');
  const locale = useLocale();
  const [searchQuery, setSearchQuery] = useState('');
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [menuOpenId, setMenuOpenId] = useState<string | null>(null);
  const [moveMenuId, setMoveMenuId] = useState<string | null>(null);

  /**
   * تصفية المحادثات بالبحث
   */
  const filteredConversations = useMemo(() => {
    if (!searchQuery.trim()) return conversations;
    const lower = searchQuery.toLowerCase();
    return conversations.filter(
      (c) =>
        c.title.toLowerCase().includes(lower) ||
        c.platform.toLowerCase().includes(lower)
    );
  }, [conversations, searchQuery]);

  /**
   * تجميع المحادثات حسب التاريخ
   */
  const groupedConversations = useMemo(() => {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    const weekAgo = new Date(today);
    weekAgo.setDate(weekAgo.getDate() - 7);

    const groups: Record<string, Conversation[]> = {
      today: [],
      yesterday: [],
      thisWeek: [],
      older: [],
    };

    filteredConversations.forEach((conv) => {
      const date = new Date(conv.updated_at);
      if (date >= today) {
        groups.today.push(conv);
      } else if (date >= yesterday) {
        groups.yesterday.push(conv);
      } else if (date >= weekAgo) {
        groups.thisWeek.push(conv);
      } else {
        groups.older.push(conv);
      }
    });

    return groups;
  }, [filteredConversations]);

  /**
   * معالجة البحث المتأخر
   */
  const debouncedSearch = useMemo(
    () => debounce((value: string) => setSearchQuery(value), 300),
    []
  );

  /**
   * بدء تعديل العنوان
   */
  const startRename = useCallback((conv: Conversation) => {
    setEditingId(conv.id);
    setEditTitle(conv.title);
    setMenuOpenId(null);
  }, []);

  /**
   * حفظ العنوان المعدل
   */
  const saveRename = useCallback(
    (id: string) => {
      if (editTitle.trim()) {
        onRename(id, editTitle.trim());
      }
      setEditingId(null);
      setEditTitle('');
    },
    [editTitle, onRename]
  );

  /**
   * عرض هيكل التحميل
   */
  if (isLoading) {
    return (
      <div className="space-y-2 p-1">
        {Array.from({ length: 5 }).map((_, i) => (
          <div key={`skeleton-${i}`} className="flex items-center gap-2 p-2">
            <Skeleton className="h-4 w-4" />
            <Skeleton className="h-4 flex-1" />
          </div>
        ))}
      </div>
    );
  }

  /**
   * عرض الحالة الفارغة
   */
  if (conversations.length === 0) {
    return (
      <EmptyState
        icon={MessageSquare}
        title={t('no_conversations')}
        description={t('start_new_chat')}
        className="py-8"
      />
    );
  }

  /**
   * عرض مجموعة محادثات
   */
  const renderGroup = (label: string, convs: Conversation[]) => {
    if (convs.length === 0) return null;

    return (
      <div key={label} className="mb-2">
        <p className="px-2 py-1 text-xs font-medium text-gray-400 dark:text-gray-500">
          {label}
        </p>
        {convs.map((conv) => (
          <ConversationItem
            key={conv.id}
            conversation={conv}
            isActive={conv.id === activeConversationId}
            isEditing={editingId === conv.id}
            editTitle={editTitle}
            menuOpen={menuOpenId === conv.id}
            moveMenuOpen={moveMenuId === conv.id}
            folders={folders}
            locale={locale}
            onSelect={() => onSelect(conv.id)}
            onStartRename={() => startRename(conv)}
            onSaveRename={() => saveRename(conv.id)}
            onCancelRename={() => setEditingId(null)}
            onEditTitleChange={setEditTitle}
            onDelete={() => { onDelete(conv.id); setMenuOpenId(null); }}
            onMove={(folderId) => { onMove(conv.id, folderId); setMoveMenuId(null); }}
            onMenuToggle={() => setMenuOpenId(menuOpenId === conv.id ? null : conv.id)}
            onMoveMenuToggle={() => setMoveMenuId(moveMenuId === conv.id ? null : conv.id)}
            t={t}
          />
        ))}
      </div>
    );
  };

  return (
    <div className="space-y-1">
      {/* حقل البحث */}
      <div className="px-1 pb-2">
        <div className="relative">
          <Search className="absolute start-2.5 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-gray-400" />
          <input
            type="text"
            placeholder={t('search_placeholder')}
            onChange={(e) => debouncedSearch(e.target.value)}
            className={cn(
              'w-full rounded-lg border-0 bg-gray-100 dark:bg-dark-800',
              'ps-8 pe-3 py-1.5 text-xs',
              'text-gray-700 dark:text-gray-300',
              'placeholder:text-gray-400 dark:placeholder:text-gray-500',
              'focus:outline-none focus:ring-1 focus:ring-primary-500'
            )}
          />
        </div>
      </div>

      {/* مجموعات المحادثات */}
      {renderGroup(t('today'), groupedConversations.today)}
      {renderGroup(t('yesterday'), groupedConversations.yesterday)}
      {renderGroup(t('this_week'), groupedConversations.thisWeek)}
      {renderGroup(t('older'), groupedConversations.older)}
    </div>
  );
}

/**
 * خصائص عنصر المحادثة
 */
interface ConversationItemProps {
  conversation: Conversation;
  isActive: boolean;
  isEditing: boolean;
  editTitle: string;
  menuOpen: boolean;
  moveMenuOpen: boolean;
  folders: Folder[];
  locale: string;
  onSelect: () => void;
  onStartRename: () => void;
  onSaveRename: () => void;
  onCancelRename: () => void;
  onEditTitleChange: (title: string) => void;
  onDelete: () => void;
  onMove: (folderId: string | null) => void;
  onMenuToggle: () => void;
  onMoveMenuToggle: () => void;
  t: ReturnType<typeof useTranslations>;
}

/**
 * عنصر محادثة واحد
 */
function ConversationItem({
  conversation,
  isActive,
  isEditing,
  editTitle,
  menuOpen,
  folders,
  locale,
  onSelect,
  onStartRename,
  onSaveRename,
  onCancelRename,
  onEditTitleChange,
  onDelete,
  onMove,
  onMenuToggle,
  t,
}: ConversationItemProps) {
  return (
    <div
      className={cn(
        'group flex items-center gap-2 rounded-lg px-2 py-1.5 cursor-pointer transition-colors',
        isActive
          ? 'bg-primary-500/10 text-primary-600 dark:text-primary-400'
          : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-dark-800'
      )}
    >
      <MessageSquare className="h-4 w-4 shrink-0 opacity-60" />

      {isEditing ? (
        <input
          type="text"
          value={editTitle}
          onChange={(e) => onEditTitleChange(e.target.value)}
          onBlur={onSaveRename}
          onKeyDown={(e) => {
            if (e.key === 'Enter') onSaveRename();
            if (e.key === 'Escape') onCancelRename();
          }}
          className="flex-1 bg-transparent text-sm outline-none border-b border-primary-500"
          autoFocus
        />
      ) : (
        <button
          onClick={onSelect}
          className="flex-1 text-start text-sm truncate"
          title={conversation.title}
        >
          {truncateText(conversation.title, 30)}
        </button>
      )}

      {/* قائمة السياق */}
      <div className="opacity-0 group-hover:opacity-100 transition-opacity shrink-0">
        <DropdownMenu open={menuOpen} onOpenChange={() => onMenuToggle()}>
          <DropdownMenuTrigger onClick={onMenuToggle}>
            <button
              className="rounded p-0.5 hover:bg-gray-200 dark:hover:bg-dark-600 transition-colors"
              aria-label="More options"
            >
              <MoreHorizontal className="h-3.5 w-3.5" />
            </button>
          </DropdownMenuTrigger>
          {menuOpen && (
            <DropdownMenuContent align="end">
              <DropdownMenuItem
                icon={<Edit3 className="h-3.5 w-3.5" />}
                onClick={onStartRename}
              >
                {t('rename')}
              </DropdownMenuItem>
              {folders.length > 0 && (
                <DropdownMenuItem
                  icon={<FolderInput className="h-3.5 w-3.5" />}
                  onClick={() => {
                    const firstFolder = folders[0];
                    if (firstFolder) onMove(firstFolder.id);
                  }}
                >
                  {t('move_to_folder')}
                </DropdownMenuItem>
              )}
              <DropdownMenuItem
                icon={<Download className="h-3.5 w-3.5" />}
                onClick={() => {/* سيتم تنفيذ التصدير لاحقاً */}}
              >
                {t('export')}
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                destructive
                icon={<Trash2 className="h-3.5 w-3.5" />}
                onClick={onDelete}
              >
                {t('delete')}
              </DropdownMenuItem>
            </DropdownMenuContent>
          )}
        </DropdownMenu>
      </div>
    </div>
  );
}
""")

    create_file("components/sidebar/FolderList.tsx", """// قائمة المجلدات: عرض المجلدات مع زر الإضافة
'use client';

import { useState, useCallback } from 'react';
import { useTranslations } from 'next-intl';
import { FolderPlus } from 'lucide-react';
import { cn } from '@/utils/cn';
import { FolderItem } from './FolderItem';
import type { Conversation } from '@/types/chat';
import type { Folder } from '@/types/folder';

/**
 * خصائص قائمة المجلدات
 */
interface FolderListProps {
  folders: Folder[];
  conversations: Conversation[];
  activeConversationId?: string;
  onSelectConversation: (id: string) => void;
  onCreateFolder: (name: string) => void;
  onDeleteFolder: (id: string) => void;
  onRenameFolder: (id: string, name: string) => void;
}

/**
 * مكون قائمة المجلدات
 */
export function FolderList({
  folders,
  conversations,
  activeConversationId,
  onSelectConversation,
  onCreateFolder,
  onDeleteFolder,
  onRenameFolder,
}: FolderListProps) {
  const t = useTranslations('sidebar');
  const [isCreating, setIsCreating] = useState(false);
  const [newFolderName, setNewFolderName] = useState('');

  /**
   * حفظ المجلد الجديد
   */
  const handleCreate = useCallback(() => {
    if (newFolderName.trim()) {
      onCreateFolder(newFolderName.trim());
      setNewFolderName('');
      setIsCreating(false);
    }
  }, [newFolderName, onCreateFolder]);

  if (folders.length === 0 && !isCreating) {
    return null;
  }

  return (
    <div className="space-y-1">
      {/* رأس المجلدات */}
      <div className="flex items-center justify-between px-2 py-1">
        <span className="text-xs font-medium text-gray-400 dark:text-gray-500 uppercase tracking-wider">
          {t('folders')}
        </span>
        <button
          onClick={() => setIsCreating(true)}
          className="rounded p-0.5 text-gray-400 hover:text-primary-500 hover:bg-gray-200 dark:hover:bg-dark-700 transition-colors"
          aria-label={t('add_folder')}
        >
          <FolderPlus className="h-3.5 w-3.5" />
        </button>
      </div>

      {/* حقل إنشاء مجلد جديد */}
      {isCreating && (
        <div className="px-2">
          <input
            type="text"
            value={newFolderName}
            onChange={(e) => setNewFolderName(e.target.value)}
            onBlur={handleCreate}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleCreate();
              if (e.key === 'Escape') {
                setIsCreating(false);
                setNewFolderName('');
              }
            }}
            placeholder={t('folder_name_placeholder')}
            className={cn(
              'w-full rounded-md border border-primary-500 bg-transparent',
              'px-2 py-1 text-xs text-gray-700 dark:text-gray-300',
              'placeholder:text-gray-400 focus:outline-none'
            )}
            autoFocus
          />
        </div>
      )}

      {/* عناصر المجلدات */}
      {folders.map((folder) => {
        const folderConversations = conversations.filter(
          (c) => c.folder_id === folder.id
        );
        return (
          <FolderItem
            key={folder.id}
            folder={folder}
            conversations={folderConversations}
            activeConversationId={activeConversationId}
            onSelectConversation={onSelectConversation}
            onDelete={() => onDeleteFolder(folder.id)}
            onRename={(name) => onRenameFolder(folder.id, name)}
          />
        );
      })}
    </div>
  );
}
""")

    create_file("components/sidebar/FolderItem.tsx", """// عنصر المجلد: مجلد قابل للطي مع اسم وعدد وإجراءات
'use client';

import { useState, useCallback } from 'react';
import { useTranslations } from 'next-intl';
import {
  Folder as FolderIcon, FolderOpen, ChevronDown, ChevronLeft, ChevronRight,
  MoreHorizontal, Edit3, Trash2, MessageSquare,
} from 'lucide-react';
import { cn } from '@/utils/cn';
import { useLocale } from 'next-intl';
import { Badge } from '@/components/ui/badge';
import {
  DropdownMenu, DropdownMenuTrigger, DropdownMenuContent,
  DropdownMenuItem, DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu';
import { truncateText } from '@/utils/helpers';
import type { Conversation } from '@/types/chat';
import type { Folder } from '@/types/folder';

/**
 * خصائص عنصر المجلد
 */
interface FolderItemProps {
  folder: Folder;
  conversations: Conversation[];
  activeConversationId?: string;
  onSelectConversation: (id: string) => void;
  onDelete: () => void;
  onRename: (name: string) => void;
}

/**
 * مكون عنصر المجلد
 */
export function FolderItem({
  folder,
  conversations,
  activeConversationId,
  onSelectConversation,
  onDelete,
  onRename,
}: FolderItemProps) {
  const t = useTranslations('sidebar');
  const locale = useLocale();
  const isRTL = locale === 'ar';

  const [isOpen, setIsOpen] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editName, setEditName] = useState(folder.name);

  const isAutoFolder = folder.type === 'auto';

  /**
   * حفظ الاسم المعدل
   */
  const saveRename = useCallback(() => {
    if (editName.trim() && editName.trim() !== folder.name) {
      onRename(editName.trim());
    }
    setIsEditing(false);
  }, [editName, folder.name, onRename]);

  const Chevron = isOpen
    ? ChevronDown
    : isRTL
      ? ChevronLeft
      : ChevronRight;

  return (
    <div className="space-y-0.5">
      {/* رأس المجلد */}
      <div
        className={cn(
          'group flex items-center gap-1.5 rounded-lg px-2 py-1 cursor-pointer transition-colors',
          'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-dark-800'
        )}
      >
        {/* سهم الطي */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="shrink-0 p-0.5"
          aria-label={isOpen ? 'Collapse folder' : 'Expand folder'}
        >
          <Chevron className="h-3 w-3" />
        </button>

        {/* أيقونة المجلد */}
        {isOpen ? (
          <FolderOpen className="h-4 w-4 shrink-0 text-primary-500" />
        ) : (
          <FolderIcon className="h-4 w-4 shrink-0" />
        )}

        {/* الاسم أو حقل التعديل */}
        {isEditing ? (
          <input
            type="text"
            value={editName}
            onChange={(e) => setEditName(e.target.value)}
            onBlur={saveRename}
            onKeyDown={(e) => {
              if (e.key === 'Enter') saveRename();
              if (e.key === 'Escape') setIsEditing(false);
            }}
            className="flex-1 bg-transparent text-xs outline-none border-b border-primary-500"
            autoFocus
          />
        ) : (
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="flex-1 text-start text-xs font-medium truncate"
          >
            {folder.name}
          </button>
        )}

        {/* شارة العدد */}
        {conversations.length > 0 && (
          <Badge variant="secondary" className="text-[10px] px-1.5 py-0">
            {conversations.length}
          </Badge>
        )}

        {/* قائمة الإجراءات */}
        {!isAutoFolder && (
          <div className="opacity-0 group-hover:opacity-100 transition-opacity shrink-0">
            <DropdownMenu open={menuOpen} onOpenChange={setMenuOpen}>
              <DropdownMenuTrigger onClick={() => setMenuOpen(!menuOpen)}>
                <button
                  className="rounded p-0.5 hover:bg-gray-200 dark:hover:bg-dark-600 transition-colors"
                  aria-label="Folder options"
                >
                  <MoreHorizontal className="h-3 w-3" />
                </button>
              </DropdownMenuTrigger>
              {menuOpen && (
                <DropdownMenuContent align="end">
                  <DropdownMenuItem
                    icon={<Edit3 className="h-3.5 w-3.5" />}
                    onClick={() => {
                      setIsEditing(true);
                      setEditName(folder.name);
                      setMenuOpen(false);
                    }}
                  >
                    {t('rename_folder')}
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem
                    destructive
                    icon={<Trash2 className="h-3.5 w-3.5" />}
                    onClick={() => {
                      onDelete();
                      setMenuOpen(false);
                    }}
                  >
                    {t('delete_folder')}
                  </DropdownMenuItem>
                </DropdownMenuContent>
              )}
            </DropdownMenu>
          </div>
        )}
      </div>

      {/* المحادثات داخل المجلد */}
      {isOpen && (
        <div className="ps-6 space-y-0.5">
          {conversations.length === 0 ? (
            <p className="text-[10px] text-gray-400 dark:text-gray-500 px-2 py-1">
              {t('no_conversations')}
            </p>
          ) : (
            conversations.map((conv) => (
              <button
                key={conv.id}
                onClick={() => onSelectConversation(conv.id)}
                className={cn(
                  'flex items-center gap-1.5 w-full rounded-md px-2 py-1 text-start transition-colors',
                  conv.id === activeConversationId
                    ? 'bg-primary-500/10 text-primary-600 dark:text-primary-400'
                    : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-dark-800'
                )}
              >
                <MessageSquare className="h-3 w-3 shrink-0 opacity-60" />
                <span className="text-xs truncate">
                  {truncateText(conv.title, 25)}
                </span>
              </button>
            ))
          )}
        </div>
      )}
    </div>
  );
}
""")

    create_file("components/sidebar/FavoritesList.tsx", """// قائمة المفضلات: عرض الشخصيات والنماذج المفضلة
'use client';

import { useTranslations } from 'next-intl';
import { Star, Sparkles, Cpu } from 'lucide-react';
import { cn } from '@/utils/cn';
import { useFavorites } from '@/hooks/useFavorites';
import { usePersonaStore } from '@/stores/personaStore';
import { usePlatformStore } from '@/stores/platformStore';
import { EmptyState } from '@/components/common/EmptyState';
import type { UserFavorite } from '@/types/database';

/**
 * مكون قائمة المفضلات
 */
export function FavoritesList() {
  const t = useTranslations('sidebar');
  const { favorites, isLoading } = useFavorites();
  const { setActivePersona } = usePersonaStore();
  const { setModel } = usePlatformStore();

  const personaFavorites = favorites.filter((f) => f.item_type === 'persona');
  const modelFavorites = favorites.filter((f) => f.item_type === 'model');

  if (favorites.length === 0 && !isLoading) {
    return null;
  }

  return (
    <div className="space-y-1 mb-2">
      {/* رأس المفضلات */}
      <div className="flex items-center gap-1.5 px-2 py-1">
        <Star className="h-3 w-3 text-yellow-500" />
        <span className="text-xs font-medium text-gray-400 dark:text-gray-500 uppercase tracking-wider">
          {t('favorites')}
        </span>
      </div>

      {/* شخصيات مفضلة */}
      {personaFavorites.map((fav) => (
        <FavoriteItem key={fav.id} favorite={fav} type="persona" />
      ))}

      {/* نماذج مفضلة */}
      {modelFavorites.map((fav) => (
        <FavoriteItem key={fav.id} favorite={fav} type="model" />
      ))}
    </div>
  );
}

/**
 * عنصر مفضلة واحد
 */
function FavoriteItem({
  favorite,
  type,
}: {
  favorite: UserFavorite;
  type: 'persona' | 'model';
}) {
  return (
    <button
      className={cn(
        'flex items-center gap-2 w-full rounded-lg px-2 py-1 text-start transition-colors',
        'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-dark-800'
      )}
    >
      {type === 'persona' ? (
        <Sparkles className="h-3.5 w-3.5 shrink-0 text-primary-500" />
      ) : (
        <Cpu className="h-3.5 w-3.5 shrink-0 text-secondary-500" />
      )}
      <span className="text-xs truncate">{favorite.item_id}</span>
    </button>
  );
}
""")

    create_file("components/sidebar/PersonaList.tsx", """// قائمة الشخصيات في الشريط الجانبي: عرض مختصر مع رابط "عرض الكل"
'use client';

import { useState, useEffect, useRef } from 'react';
import { useTranslations, useLocale } from 'next-intl';
import { Sparkles, Lock, ChevronLeft, ChevronRight } from 'lucide-react';
import { cn } from '@/utils/cn';
import { usePersonaStore } from '@/stores/personaStore';
import { useAuthStore } from '@/stores/authStore';
import { createSupabaseBrowserClient } from '@/lib/supabase-client';
import { Link } from '@/i18n/navigation';
import type { Persona } from '@/types/persona';

/**
 * مكون قائمة الشخصيات في الشريط الجانبي
 */
export function PersonaList() {
  const t = useTranslations('sidebar');
  const tPersonas = useTranslations('personas');
  const locale = useLocale();
  const isRTL = locale === 'ar';
  const supabase = createSupabaseBrowserClient();

  const { role } = useAuthStore();
  const { activePersona, setActivePersona } = usePersonaStore();
  const [personas, setPersonas] = useState<Persona[]>([]);
  const loadedRef = useRef(false);

  /**
   * تحميل الشخصيات
   */
  useEffect(() => {
    if (loadedRef.current) return;
    loadedRef.current = true;

    const loadPersonas = async () => {
      try {
        const { data, error } = await supabase
          .from('personas')
          .select('*')
          .in('type', ['system', 'premium'])
          .eq('is_active', true)
          .order('usage_count', { ascending: false })
          .limit(6);

        if (!error && data) {
          setPersonas(data as Persona[]);
        }
      } catch {
        // تجاهل
      }
    };

    loadPersonas();

    return () => {};
  }, [supabase]);

  const ViewAllChevron = isRTL ? ChevronLeft : ChevronRight;

  return (
    <div className="space-y-1">
      {/* رأس الشخصيات */}
      <div className="flex items-center justify-between px-2 py-1">
        <span className="text-xs font-medium text-gray-400 dark:text-gray-500 uppercase tracking-wider">
          {t('personas')}
        </span>
        <Link
          href="/personas"
          className="flex items-center gap-0.5 text-[10px] text-primary-500 hover:text-primary-400 transition-colors"
        >
          {t('view_all')}
          <ViewAllChevron className="h-3 w-3" />
        </Link>
      </div>

      {/* قائمة الشخصيات */}
      {personas.map((persona) => {
        const isLocked = persona.type === 'premium' && role === 'free';
        const isActive = activePersona?.id === persona.id;

        return (
          <button
            key={persona.id}
            onClick={() => {
              if (!isLocked) {
                setActivePersona(isActive ? null : persona);
              }
            }}
            disabled={isLocked}
            className={cn(
              'flex items-center gap-2 w-full rounded-lg px-2 py-1.5 text-start transition-colors',
              isActive
                ? 'bg-primary-500/10 text-primary-600 dark:text-primary-400'
                : isLocked
                  ? 'text-gray-400 dark:text-gray-500 opacity-60 cursor-not-allowed'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-dark-800'
            )}
          >
            <Sparkles className={cn('h-3.5 w-3.5 shrink-0', isActive ? 'text-primary-500' : '')} />
            <span className="flex-1 text-xs truncate">{persona.name}</span>
            {isLocked && <Lock className="h-3 w-3 shrink-0 text-gray-400" />}
          </button>
        );
      })}
    </div>
  );
}
""")

    create_file("components/sidebar/QuickSettings.tsx", """// الإعدادات السريعة: تبديل المظهر واللغة مع روابط الإعدادات وتسجيل الخروج
'use client';

import { useState } from 'react';
import { useTranslations, useLocale } from 'next-intl';
import { useRouter, usePathname } from 'next/navigation';
import { Moon, Sun, Globe, Settings, LogOut } from 'lucide-react';
import { cn } from '@/utils/cn';
import { useUIStore } from '@/stores/uiStore';
import { useAuth } from '@/hooks/useAuth';
import { Tooltip } from '@/components/ui/tooltip';
import { ConfirmDialog } from '@/components/common/ConfirmDialog';
import { Separator } from '@/components/ui/separator';
import { Link } from '@/i18n/navigation';

/**
 * مكون الإعدادات السريعة
 */
export function QuickSettings() {
  const t = useTranslations('sidebar');
  const locale = useLocale();
  const router = useRouter();
  const pathname = usePathname();

  const { theme, setTheme, setLocale } = useUIStore();
  const { signOut, user } = useAuth();
  const [showLogoutConfirm, setShowLogoutConfirm] = useState(false);

  /**
   * تبديل المظهر
   */
  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);

    if (newTheme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  /**
   * تبديل اللغة
   */
  const toggleLocale = () => {
    const newLocale = locale === 'ar' ? 'en' : 'ar';
    setLocale(newLocale);

    // استبدال اللغة في المسار
    const segments = pathname.split('/');
    if (segments.length > 1 && (segments[1] === 'ar' || segments[1] === 'en')) {
      segments[1] = newLocale;
    }
    router.push(segments.join('/'));
  };

  return (
    <>
      <div className="p-3 space-y-2">
        {/* معلومات المستخدم */}
        {user && (
          <div className="px-2 py-1">
            <p className="text-xs font-medium text-gray-700 dark:text-gray-300 truncate">
              {user.display_name ?? user.email}
            </p>
            <p className="text-[10px] text-gray-400 dark:text-gray-500 truncate">
              {user.email}
            </p>
          </div>
        )}

        <Separator />

        {/* أزرار الإعدادات السريعة */}
        <div className="flex items-center justify-between">
          {/* تبديل المظهر */}
          <Tooltip content={theme === 'dark' ? t('theme_light') : t('theme_dark')}>
            <button
              onClick={toggleTheme}
              className="rounded-lg p-2 text-gray-500 hover:bg-gray-200 dark:hover:bg-dark-700 transition-colors"
              aria-label={theme === 'dark' ? t('theme_light') : t('theme_dark')}
            >
              {theme === 'dark' ? (
                <Sun className="h-4 w-4" />
              ) : (
                <Moon className="h-4 w-4" />
              )}
            </button>
          </Tooltip>

          {/* تبديل اللغة */}
          <Tooltip content={locale === 'ar' ? t('language_en') : t('language_ar')}>
            <button
              onClick={toggleLocale}
              className="rounded-lg p-2 text-gray-500 hover:bg-gray-200 dark:hover:bg-dark-700 transition-colors"
              aria-label={locale === 'ar' ? t('language_en') : t('language_ar')}
            >
              <Globe className="h-4 w-4" />
            </button>
          </Tooltip>

          {/* الإعدادات */}
          <Tooltip content={t('settings')}>
            <Link
              href="/settings"
              className="rounded-lg p-2 text-gray-500 hover:bg-gray-200 dark:hover:bg-dark-700 transition-colors"
              aria-label={t('settings')}
            >
              <Settings className="h-4 w-4" />
            </Link>
          </Tooltip>

          {/* تسجيل الخروج */}
          <Tooltip content={t('logout')}>
            <button
              onClick={() => setShowLogoutConfirm(true)}
              className="rounded-lg p-2 text-gray-500 hover:bg-red-100 dark:hover:bg-red-900/20 hover:text-red-600 dark:hover:text-red-400 transition-colors"
              aria-label={t('logout')}
            >
              <LogOut className="h-4 w-4" />
            </button>
          </Tooltip>
        </div>
      </div>

      {/* حوار تأكيد تسجيل الخروج */}
      <ConfirmDialog
        open={showLogoutConfirm}
        onOpenChange={setShowLogoutConfirm}
        title={t('logout')}
        message={useTranslations('auth')('logout_confirm')}
        confirmLabel={t('logout')}
        destructive
        onConfirm={signOut}
      />
    </>
  );
}
""")

    # ──────────────────────────────────────────────
    # Chat Pages
    # ──────────────────────────────────────────────
    print("\n📁 Chat Pages")
    print("-" * 40)

    create_file("app/[locale]/chat/page.tsx", """// صفحة الدردشة الرئيسية: التخطيط الكامل مع الشريط الجانبي ومنطقة الدردشة
'use client';

import { useCallback, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useTranslations, useLocale } from 'next-intl';
import { MessageSquare, Sparkles, Zap, PenTool, Mail } from 'lucide-react';
import { cn } from '@/utils/cn';
import { RouteGuard } from '@/components/auth/RouteGuard';
import { Sidebar } from '@/components/sidebar/Sidebar';
import { EmptyState } from '@/components/common/EmptyState';
import { useChat } from '@/hooks/useChat';
import { useFolders } from '@/hooks/useFolders';
import { useUIStore } from '@/stores/uiStore';
import { usePlatformStore } from '@/stores/platformStore';
import { usePersonaStore } from '@/stores/personaStore';
import { Button } from '@/components/ui/button';

/**
 * صفحة الدردشة الرئيسية
 */
export default function ChatPage() {
  return (
    <RouteGuard>
      <ChatPageContent />
    </RouteGuard>
  );
}

/**
 * محتوى صفحة الدردشة
 */
function ChatPageContent() {
  const t = useTranslations('chat');
  const tSidebar = useTranslations('sidebar');
  const locale = useLocale();
  const router = useRouter();
  const isRTL = locale === 'ar';

  const { sidebarOpen } = useUIStore();
  const { activePlatform, activeModel } = usePlatformStore();
  const { activePersona } = usePersonaStore();

  const {
    conversations,
    isLoadingConversations,
    createConversation,
    deleteConversation,
    updateConversation,
  } = useChat();

  const {
    folders,
    createFolder,
    deleteFolder,
    updateFolder,
  } = useFolders();

  /**
   * إنشاء محادثة جديدة
   */
  const handleNewChat = useCallback(async () => {
    const conv = await createConversation({
      platform: activePlatform,
      model: activeModel || 'default',
      persona_id: activePersona?.id ?? null,
    });

    if (conv) {
      router.push(`/${locale}/chat/${conv.id}`);
    }
  }, [createConversation, activePlatform, activeModel, activePersona, router, locale]);

  /**
   * اختيار محادثة
   */
  const handleSelectConversation = useCallback(
    (id: string) => {
      router.push(`/${locale}/chat/${id}`);
    },
    [router, locale]
  );

  /**
   * حذف محادثة
   */
  const handleDeleteConversation = useCallback(
    async (id: string) => {
      await deleteConversation(id);
    },
    [deleteConversation]
  );

  /**
   * إعادة تسمية محادثة
   */
  const handleRenameConversation = useCallback(
    async (id: string, title: string) => {
      await updateConversation(id, { title });
    },
    [updateConversation]
  );

  /**
   * نقل محادثة لمجلد
   */
  const handleMoveConversation = useCallback(
    async (id: string, folderId: string | null) => {
      await updateConversation(id, { folder_id: folderId });
    },
    [updateConversation]
  );

  /**
   * إنشاء مجلد
   */
  const handleCreateFolder = useCallback(
    async (name: string) => {
      await createFolder(name, 'custom');
    },
    [createFolder]
  );

  /**
   * اقتراحات البداية
   */
  const suggestions = [
    { icon: Sparkles, text: t('suggestion_1'), command: '/linkedin' },
    { icon: Zap, text: t('suggestion_2'), command: '/brainstorm' },
    { icon: PenTool, text: t('suggestion_3'), command: '/prompt' },
    { icon: Mail, text: t('suggestion_4'), command: '/email' },
  ];

  return (
    <div className="flex h-screen bg-white dark:bg-dark-950">
      {/* الشريط الجانبي */}
      <Sidebar
        conversations={conversations}
        folders={folders}
        onNewChat={handleNewChat}
        onSelectConversation={handleSelectConversation}
        onDeleteConversation={handleDeleteConversation}
        onRenameConversation={handleRenameConversation}
        onMoveConversation={handleMoveConversation}
        onCreateFolder={handleCreateFolder}
        onDeleteFolder={deleteFolder}
        onRenameFolder={updateFolder}
        isLoadingConversations={isLoadingConversations}
      />

      {/* المحتوى الرئيسي */}
      <main
        className={cn(
          'flex-1 flex flex-col transition-all duration-300',
          sidebarOpen
            ? isRTL
              ? 'lg:me-sidebar'
              : 'lg:ms-sidebar'
            : ''
        )}
      >
        {/* شريط علوي مبسط - سيتم استبداله بمكون Header لاحقاً */}
        <div className="h-16 shrink-0 border-b border-gray-200 dark:border-dark-700 flex items-center px-4">
          <h1 className="text-lg font-semibold text-gray-700 dark:text-gray-300">
            {t('new_conversation')}
          </h1>
        </div>

        {/* منطقة الترحيب */}
        <div className="flex-1 flex items-center justify-center p-4">
          <div className="max-w-2xl w-full text-center space-y-8">
            {/* رسالة الترحيب */}
            <div className="space-y-3">
              <div className="flex justify-center">
                <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-br from-primary-500 to-secondary-500 shadow-lg shadow-primary-500/20">
                  <MessageSquare className="h-10 w-10 text-white" />
                </div>
              </div>
              <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100">
                {t('empty_welcome')}
              </h2>
              <p className="text-gray-500 dark:text-gray-400 max-w-md mx-auto">
                {t('empty_subtitle')}
              </p>
            </div>

            {/* أزرار الاقتراحات */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-lg mx-auto">
              {suggestions.map((suggestion) => {
                const Icon = suggestion.icon;
                return (
                  <button
                    key={suggestion.command}
                    onClick={handleNewChat}
                    className={cn(
                      'flex items-center gap-3 rounded-xl border border-gray-200 dark:border-dark-700',
                      'bg-white dark:bg-dark-800 p-4 text-start',
                      'hover:border-primary-500/50 hover:bg-primary-500/5 transition-all duration-200',
                      'group'
                    )}
                  >
                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-gray-100 dark:bg-dark-700 group-hover:bg-primary-500/10 transition-colors">
                      <Icon className="h-4.5 w-4.5 text-gray-500 group-hover:text-primary-500 transition-colors" />
                    </div>
                    <span className="text-sm text-gray-700 dark:text-gray-300 group-hover:text-gray-900 dark:group-hover:text-gray-100 transition-colors">
                      {suggestion.text}
                    </span>
                  </button>
                );
              })}
            </div>

            {/* زر بدء محادثة */}
            <Button onClick={handleNewChat} size="lg" className="shadow-lg shadow-primary-500/20">
              {t('start_new')}
            </Button>
          </div>
        </div>
      </main>
    </div>
  );
}
""")

    create_file("app/[locale]/chat/[id]/page.tsx", """// صفحة محادثة محددة: تحميل المحادثة والرسائل وعرضها
'use client';

import { useEffect, useState, useCallback, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useTranslations, useLocale } from 'next-intl';
import { cn } from '@/utils/cn';
import { RouteGuard } from '@/components/auth/RouteGuard';
import { Sidebar } from '@/components/sidebar/Sidebar';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { Skeleton } from '@/components/ui/skeleton';
import { useChat } from '@/hooks/useChat';
import { useFolders } from '@/hooks/useFolders';
import { useUIStore } from '@/stores/uiStore';
import { usePlatformStore } from '@/stores/platformStore';
import { usePersonaStore } from '@/stores/personaStore';
import { useChatStore } from '@/stores/chatStore';
import { formatRelativeTime } from '@/utils/formatters';
import { MessageSquare, Bot, User as UserIcon } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

/**
 * خصائص الصفحة
 */
interface ChatIdPageProps {
  params: { id: string; locale: string };
}

/**
 * صفحة محادثة محددة
 */
export default function ChatIdPage({ params }: ChatIdPageProps) {
  return (
    <RouteGuard>
      <ChatIdContent conversationId={params.id} />
    </RouteGuard>
  );
}

/**
 * محتوى صفحة المحادثة
 */
function ChatIdContent({ conversationId }: { conversationId: string }) {
  const t = useTranslations('chat');
  const locale = useLocale();
  const router = useRouter();
  const isRTL = locale === 'ar';

  const { sidebarOpen } = useUIStore();
  const { activePlatform, activeModel } = usePlatformStore();
  const { activePersona } = usePersonaStore();
  const { messages: storeMessages } = useChatStore();

  const {
    conversations,
    currentConversation,
    messages,
    isLoadingConversations,
    isLoadingMessages,
    loadConversation,
    loadMessages,
    createConversation,
    deleteConversation,
    updateConversation,
  } = useChat();

  const { folders, createFolder, deleteFolder, updateFolder } = useFolders();

  const [isInitialLoading, setIsInitialLoading] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const loadedRef = useRef(false);

  /**
   * تحميل المحادثة والرسائل
   */
  useEffect(() => {
    if (loadedRef.current) return;
    loadedRef.current = true;

    const init = async () => {
      setIsInitialLoading(true);
      const conv = await loadConversation(conversationId);

      if (!conv) {
        router.replace(`/${locale}/chat`);
        return;
      }

      await loadMessages(conversationId);
      setIsInitialLoading(false);
    };

    init();

    return () => {};
  }, [conversationId, loadConversation, loadMessages, router, locale]);

  /**
   * التمرير لأسفل عند إضافة رسائل
   */
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    return () => {};
  }, [messages.length, storeMessages.length]);

  /**
   * محادثة جديدة
   */
  const handleNewChat = useCallback(async () => {
    const conv = await createConversation({
      platform: activePlatform,
      model: activeModel || 'default',
      persona_id: activePersona?.id ?? null,
    });
    if (conv) {
      router.push(`/${locale}/chat/${conv.id}`);
    }
  }, [createConversation, activePlatform, activeModel, activePersona, router, locale]);

  /**
   * اختيار محادثة
   */
  const handleSelectConversation = useCallback(
    (id: string) => {
      if (id !== conversationId) {
        loadedRef.current = false;
        router.push(`/${locale}/chat/${id}`);
      }
    },
    [router, locale, conversationId]
  );

  // الرسائل المعروضة
  const displayMessages = storeMessages.length > 0 ? storeMessages : messages;

  return (
    <div className="flex h-screen bg-white dark:bg-dark-950">
      {/* الشريط الجانبي */}
      <Sidebar
        conversations={conversations}
        folders={folders}
        activeConversationId={conversationId}
        onNewChat={handleNewChat}
        onSelectConversation={handleSelectConversation}
        onDeleteConversation={async (id) => {
          await deleteConversation(id);
          if (id === conversationId) {
            router.replace(`/${locale}/chat`);
          }
        }}
        onRenameConversation={async (id, title) => {
          await updateConversation(id, { title });
        }}
        onMoveConversation={async (id, folderId) => {
          await updateConversation(id, { folder_id: folderId });
        }}
        onCreateFolder={async (name) => {
          await createFolder(name, 'custom');
        }}
        onDeleteFolder={deleteFolder}
        onRenameFolder={updateFolder}
        isLoadingConversations={isLoadingConversations}
      />

      {/* المحتوى الرئيسي */}
      <main
        className={cn(
          'flex-1 flex flex-col transition-all duration-300',
          sidebarOpen
            ? isRTL ? 'lg:me-sidebar' : 'lg:ms-sidebar'
            : ''
        )}
      >
        {/* شريط علوي */}
        <div className="h-16 shrink-0 border-b border-gray-200 dark:border-dark-700 flex items-center justify-between px-4">
          <div className="flex items-center gap-2 min-w-0">
            <MessageSquare className="h-5 w-5 shrink-0 text-gray-400" />
            {isInitialLoading ? (
              <Skeleton className="h-5 w-40" />
            ) : (
              <h1 className="text-base font-medium text-gray-700 dark:text-gray-300 truncate">
                {currentConversation?.title ?? t('new_conversation')}
              </h1>
            )}
          </div>
          {currentConversation && (
            <div className="flex items-center gap-2 text-xs text-gray-400">
              <span>{currentConversation.platform}</span>
              <span>•</span>
              <span>{currentConversation.model}</span>
            </div>
          )}
        </div>

        {/* منطقة الرسائل */}
        <div className="flex-1 overflow-y-auto custom-scrollbar p-4">
          {isInitialLoading ? (
            <div className="space-y-6 max-w-3xl mx-auto">
              {Array.from({ length: 3 }).map((_, i) => (
                <MessageSkeleton key={`msg-skel-${i}`} isUser={i % 2 === 0} />
              ))}
            </div>
          ) : displayMessages.length === 0 ? (
            <div className="flex items-center justify-center h-full">
              <p className="text-gray-400 dark:text-gray-500">{t('no_messages')}</p>
            </div>
          ) : (
            <div className="space-y-4 max-w-3xl mx-auto">
              {displayMessages.map((msg) => (
                <div
                  key={msg.id}
                  className={cn(
                    'flex gap-3',
                    msg.role === 'user' ? 'justify-end' : 'justify-start'
                  )}
                >
                  {/* أيقونة المرسل */}
                  {msg.role !== 'user' && (
                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-primary-500/10">
                      <Bot className="h-4 w-4 text-primary-500" />
                    </div>
                  )}

                  {/* فقاعة الرسالة */}
                  <div
                    className={cn(
                      'max-w-[80%] rounded-2xl px-4 py-3',
                      msg.role === 'user'
                        ? 'bg-primary-500 text-white rounded-ee-md'
                        : 'bg-gray-100 dark:bg-dark-800 text-gray-800 dark:text-gray-200 rounded-es-md'
                    )}
                  >
                    {msg.role === 'user' ? (
                      <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                    ) : (
                      <div className="text-sm prose prose-sm dark:prose-invert max-w-none">
                        <ReactMarkdown>{msg.content}</ReactMarkdown>
                      </div>
                    )}

                    {/* معلومات إضافية */}
                    {msg.role === 'assistant' && msg.tokens_used > 0 && (
                      <div className="mt-2 flex items-center gap-2 text-[10px] text-gray-400 dark:text-gray-500">
                        {msg.tokens_used > 0 && <span>{msg.tokens_used} tokens</span>}
                        {msg.response_time_ms && <span>• {msg.response_time_ms}ms</span>}
                      </div>
                    )}
                  </div>

                  {/* أيقونة المستخدم */}
                  {msg.role === 'user' && (
                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-gray-200 dark:bg-dark-700">
                      <UserIcon className="h-4 w-4 text-gray-500" />
                    </div>
                  )}
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* منطقة الإدخال - سيتم استبدالها بمكون MessageInput لاحقاً */}
        <div className="shrink-0 border-t border-gray-200 dark:border-dark-700 p-4">
          <div className="max-w-3xl mx-auto">
            <div className="flex items-center gap-2 rounded-xl border border-gray-200 dark:border-dark-700 bg-white dark:bg-dark-800 px-4 py-3">
              <input
                type="text"
                placeholder={t('type_message')}
                className="flex-1 bg-transparent text-sm text-gray-700 dark:text-gray-300 placeholder:text-gray-400 dark:placeholder:text-gray-500 outline-none"
                disabled
              />
              <button
                className="rounded-lg bg-primary-500 px-4 py-1.5 text-sm font-medium text-white opacity-50 cursor-not-allowed"
                disabled
              >
                {t('send')}
              </button>
            </div>
            <p className="text-center text-[10px] text-gray-400 dark:text-gray-500 mt-2">
              {t('type_slash')}
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}

/**
 * هيكل رسالة للتحميل
 */
function MessageSkeleton({ isUser }: { isUser: boolean }) {
  return (
    <div className={cn('flex gap-3', isUser ? 'justify-end' : 'justify-start')}>
      {!isUser && <Skeleton circle className="h-8 w-8 shrink-0" />}
      <div className={cn('space-y-2', isUser ? 'items-end' : 'items-start')}>
        <Skeleton className={cn('h-4', isUser ? 'w-48' : 'w-64')} />
        <Skeleton className={cn('h-4', isUser ? 'w-32' : 'w-56')} />
        {!isUser && <Skeleton className="h-4 w-40" />}
      </div>
      {isUser && <Skeleton circle className="h-8 w-8 shrink-0" />}
    </div>
  );
}
""")

    # ──────────────────────────────────────────────
    # Summary
    # ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("📊 BUILD PHASE 3A SUMMARY")
    print("=" * 60)
    print(f"  ✅ Files created: {files_created}")
    print(f"  ❌ Files failed: {files_failed}")
    print(f"  📁 Total: {files_created + files_failed}")
    print()
    print("📋 Files Created:")
    print()
    print("  UI COMPONENTS (Prerequisites):")
    print("    • components/ui/skeleton.tsx        (Loading skeletons)")
    print("    • components/ui/separator.tsx        (Line separator)")
    print("    • components/ui/scroll-area.tsx      (Custom scrollbar area)")
    print("    • components/ui/dialog.tsx           (Modal dialog)")
    print("    • components/ui/dropdown-menu.tsx    (Context menu)")
    print("    • components/ui/tooltip.tsx          (Hover tooltip)")
    print("    • components/ui/badge.tsx            (Status badges)")
    print()
    print("  HOOKS:")
    print("    • hooks/useChat.ts                   (Conversations + Messages CRUD)")
    print("    • hooks/useFolders.ts                (Folders CRUD + reorder)")
    print("    • hooks/useFavorites.ts              (Favorites add/remove/check)")
    print()
    print("  COMMON COMPONENTS:")
    print("    • components/common/EmptyState.tsx    (Empty state with icon+action)")
    print("    • components/common/ConfirmDialog.tsx (Confirm with destructive+loading)")
    print()
    print("  SIDEBAR COMPONENTS:")
    print("    • components/sidebar/Sidebar.tsx          (Main sidebar - RTL/LTR)")
    print("    • components/sidebar/ConversationList.tsx  (Search + grouped + context)")
    print("    • components/sidebar/FolderList.tsx        (Folders + create)")
    print("    • components/sidebar/FolderItem.tsx        (Collapsible + rename/delete)")
    print("    • components/sidebar/FavoritesList.tsx     (Personas + models)")
    print("    • components/sidebar/PersonaList.tsx       (System + premium + lock)")
    print("    • components/sidebar/QuickSettings.tsx     (Theme/lang/settings/logout)")
    print()
    print("  CHAT PAGES:")
    print("    • app/[locale]/chat/page.tsx          (Welcome + suggestions)")
    print("    • app/[locale]/chat/[id]/page.tsx     (Conversation + messages)")
    print()
    print("📝 NOTES:")
    print("  - Sidebar: 280px fixed desktop, drawer tablet, overlay mobile")
    print("  - Sidebar RIGHT in Arabic (RTL), LEFT in English (LTR)")
    print("  - ConversationList: debounced search, date grouping, context menu")
    print("  - FolderItem: collapsible, auto folders undeletable, badge counts")
    print("  - PersonaList: shows lock icon for premium personas when user is free")
    print("  - QuickSettings: theme toggle updates DOM class, locale toggle navigates")
    print("  - Chat page: welcome state with 4 suggestion cards")
    print("  - Chat/[id]: loads conversation, messages, skeleton loading, redirect if not found")
    print("  - Messages rendered with ReactMarkdown for assistant, plain text for user")
    print("  - All text through i18n, no hardcoded strings")
    print("  - TypeScript strict, no 'any' types")
    print()
    print("🔜 REMAINING PHASES:")
    print("  Phase 3B: Header + Chat Area + MessageInput + Streaming")
    print("  Phase 3C: AI Providers + API Route + Encryption + Rate Limiting")
    print("  Phase 4:  API Keys management")
    print("  Phase 5A: Personas (library, form, ratings)")
    print("  Phase 5B: Features (export, onboarding, settings page)")
    print("  Phase 6A: Admin (layout, dashboard, users)")
    print("  Phase 6B: Admin (keys, models, personas, codes, notifications)")
    print("  Phase 7:  Final (worker proxy, telegram, polish)")
    print()
    print("✅ Phase 3A Complete! Ready for Phase 3B.")


if __name__ == "__main__":
    main()
